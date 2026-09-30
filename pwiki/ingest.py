"""wiki ingest: raw source -> local Gemma -> reviewed-style Obsidian notes -> index.

Per source:
  1. copy into vault/raw/ if it isn't there (content unchanged), hash it
  2. skip if the hash matches the catalog (unless --force)
  3. send the full text + heading list + existing note titles to Gemma (JSON out)
  4. validate titles/folders/sections in code; merge into notes by title
  5. afterwards: drop broken links, rewrite index.md + Sources.md, rebuild the index
"""
import datetime as dt
import hashlib
import json
import re
import shutil
from pathlib import Path

from . import config, index, llm, notes, prompts

HEADING = re.compile(r"^#{1,6}\s+(.*)", re.M)
INGEST_CTX = 16384   # whole-document ingest; our largest source is ~6k tokens


def _load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def source_id(path):
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")


def _collect(target):
    target = Path(target)
    if target.is_dir():
        return sorted(target.glob("*.md")) + sorted(target.glob("*.txt"))
    if target.exists():
        return [target]
    raise FileNotFoundError(f"No such file or folder: {target}")


def _headings(text):
    return [h.strip() for h in HEADING.findall(text)]


def _match_heading(section, headings):
    """Map the model's section name onto a real heading (for #heading links)."""
    if not section:
        return None
    s = section.lower().strip(" #")
    for h in headings:
        if h.lower() == s:
            return h
    for h in headings:
        if s in h.lower() or h.lower() in s:
            return h
    return None


def _mentioned(title, text):
    """Cross-source link guard: a link to a note from a DIFFERENT source is kept
    only if that note's subject actually appears in this source's text."""
    words = [w for w in re.findall(r"[a-z0-9]+", title.lower()) if len(w) > 2]
    low = text.lower()
    return title.lower() in low or (words and all(w in low for w in words))


def _content_words(title):
    return {w for w in re.findall(r"[a-z0-9]+", title.lower()) if len(w) > 2}


def _same_source_match(existing, sid, title, topic):
    """Re-ingest guard (v1 fix: 'Action Space Nuance' duplicated 'Agent Action
    Space'). A concept is matched to a note that already came from THIS source
    if their titles share at least half of their content words."""
    if topic.get("_is_source"):
        return None
    words = _content_words(title)
    best, best_score = None, 0.0
    for n in existing.values():
        if sid not in n.source_ids or n.folder != "Concepts":
            continue
        other = _content_words(n.title)
        score = len(words & other) / max(len(words | other), 1)
        if score >= 0.5 and score > best_score:
            best, best_score = n, score
    return best


def run(target, force=False, model=None, log=print):
    model = model or config.CHAT_MODEL
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    catalog = _load(config.SOURCES_JSON, {})
    files = _collect(target)
    changed = 0
    for f in files:
        raw = config.RAW_DIR / f.name
        if f.resolve() != raw.resolve():
            if raw.exists() and raw.read_bytes() != f.read_bytes():
                raise RuntimeError(f"{raw} already exists with different content; originals are never overwritten")
            shutil.copy2(f, raw)                     # byte-for-byte copy, content unchanged
            log(f"+ copied {f.name} into vault/raw/ (unchanged)")
        sid = source_id(raw)
        sha = hashlib.sha256(raw.read_bytes()).hexdigest()
        prev = catalog.get(sid, {})
        if prev.get("sha256") == sha and not force:
            log(f"= {raw.name}: unchanged since last ingest, skipped (use --force to regenerate)")
            continue
        log(f"> {raw.name}: sending to {model} …")
        written = _ingest_one(raw, sid, model, log)
        catalog[sid] = {**prev, "title": raw.stem, "raw_path": f"raw/{raw.name}", "sha256": sha,
                        "ingested_at": dt.datetime.now().isoformat(timespec="seconds"),
                        "model": model, "notes": written}
        catalog[sid].setdefault("origin", "—")
        changed += 1
    config.DATA.mkdir(exist_ok=True)
    config.SOURCES_JSON.write_text(json.dumps(catalog, indent=2))
    broken = notes.fix_links(log)
    notes.write_index(catalog)
    notes.write_sources_page(catalog)
    total = len(list(config.WIKI_DIR.rglob("*.md")))
    log(f"wiki: {total} notes · {changed} source(s) processed · {broken} broken link(s) removed")
    log("rebuilding retrieval index …")
    index.build(log=log)
    return changed


def _ingest_one(raw, sid, model, log):
    text = raw.read_text(encoding="utf-8")
    headings = _headings(text)
    existing = notes.all_notes()
    existing_list = "\n".join(f"- {n.title} ({n.folder}): {n.summary[:120]}" for n in existing.values()) or "(none yet)"
    messages = [
        {"role": "system", "content": prompts.load("ingest-instructions.md")},
        {"role": "user", "content":
            f"EXISTING NOTES:\n{existing_list}\n\nSOURCE HEADINGS:\n" + "\n".join(f"- {h}" for h in headings) +
            f"\n\nSOURCE FILE: {raw.name}\n\nSOURCE TEXT:\n{text}"},
    ]
    msg, stats = llm.chat(messages, model=model, fmt="json", temperature=0.0, num_ctx=INGEST_CTX)
    log(f"  gemma: {stats['wall_s']}s, {stats['prompt_tokens']} prompt tok, {stats['output_tokens']} out tok")
    try:
        data = json.loads(msg["content"])
    except json.JSONDecodeError:
        raise RuntimeError(f"Gemma did not return valid JSON for {raw.name}; nothing was written")

    topics = [dict(data.get("source_note") or {}, _is_source=True)] + list(data.get("concepts") or [])
    link_stem = f"raw/{raw.stem}"
    accepted = {}
    for t in topics:
        title = notes.clean_title(t.get("title", ""))
        if not title:
            log(f"  ! rejected unusable title {t.get('title')!r}")
            continue
        folder = t.get("folder") if t.get("folder") in config.WIKI_FOLDERS else ("Projects" if t.get("_is_source") else "Concepts")
        accepted[title] = (t, folder)

    written = []
    source_title = next((ti for ti, (t, _) in accepted.items() if t.get("_is_source")), None)
    for title, (t, folder) in accepted.items():
        note = notes.find(existing, title) or _same_source_match(existing, sid, title, t)
        if note is None and t.get("_is_source"):
            # re-ingest: the source's main note keeps its (possibly renamed) title
            note = next((n for n in existing.values()
                         if sid in n.source_ids and n.folder in ("Projects", "Courses")), None)
        note = note or notes.Note(title=title, folder=folder)
        if t.get("_is_source"):
            source_title = note.title
        if note.reviewed and sid in note.blocks:
            log(f"  = kept reviewed note [[{note.title}]] (only links/sources refreshed)")
        else:
            lines = []
            if not t.get("_is_source") and source_title:
                lines.append(f"### In [[{source_title}]]")
            for kp in t.get("key_points") or []:
                point = (kp.get("point") if isinstance(kp, dict) else str(kp)).strip()
                h = _match_heading(kp.get("section") if isinstance(kp, dict) else None, headings)
                ref = f"[[{link_stem}#{h}|§ {h}]]" if h else f"[[{link_stem}|source]]"
                if point:
                    lines.append(f"- {point} ({ref})")
            note.blocks[sid] = "\n".join(lines)
            if not note.summary:
                note.summary = (t.get("summary") or "").strip()
        if sid not in note.source_ids:
            note.source_ids.append(sid)
        note.sources[sid] = f"- [[{link_stem}|{raw.stem}]] — original, `{sid}`"
        note.generated_by = model
        for r in t.get("related") or []:
            rt = notes.clean_title(r.get("title", "")) if isinstance(r, dict) else None
            if rt and rt.lower() != note.title.lower():
                target = notes.find(existing, rt)
                if target and sid not in target.source_ids and not _mentioned(target.title, text):
                    log(f"  ! dropped unrelated link [[{target.title}]] from [[{note.title}]]")
                    continue
                rt = target.title if target else rt
                note.related.setdefault(rt, (r.get("why") or "related topic").strip().rstrip("."))
        if source_title and note.title != source_title and not t.get("_is_source"):
            note.related.setdefault(source_title, "where this idea is applied")
        note.path.parent.mkdir(parents=True, exist_ok=True)
        note.path.write_text(note.render(), encoding="utf-8")
        existing[note.title.lower()] = note
        written.append(note.title)
        log(f"  ✓ {note.folder}/{note.title}.md")
    return written
