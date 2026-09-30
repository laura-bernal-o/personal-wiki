"""Obsidian note files: readable titles, frontmatter, per-source sections, links, index.

Idempotency: each source writes its content between `<!-- src:ID -->` markers
inside a note. Re-ingesting the same source replaces its own block instead of
appending a second copy, and titles are matched case-insensitively (plus
aliases), so no duplicate notes appear.
"""
import datetime as dt
import re
from dataclasses import dataclass, field

from . import config

WIKILINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]")
SMALL = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs"}
BAD_TITLE = re.compile(r"(\b[0-9a-f]{8,}\b|\d{4}-\d{2}-\d{2}|\bclass\s*\d|\.md$|^(how|what|why|when|which|who)\b)", re.I)


# --- titles --------------------------------------------------------------
def clean_title(raw):
    """Return a safe, readable Title Case filename stem, or None if unusable."""
    t = re.sub(r"(?<=\w)\.(?=\w)", "\x00", raw or "")          # protect "Next.js"
    t = re.sub(r"[^\w\s\-'\x00]", " ", t).replace("_", " ").replace("\x00", ".")
    t = re.sub(r"\s+", " ", t).strip(" -")
    words = t.split()
    if not 1 <= len(words) <= 6 or BAD_TITLE.search(t) or len(t) > 60:
        return None
    out = []
    for i, w in enumerate(words):
        if any(ch.isupper() for ch in w[1:]) or w.isupper():   # keep DQN, nanoGPT, BM25
            out.append(w)
        elif i and w.lower() in SMALL:
            out.append(w.lower())
        else:
            out.append(w[0].upper() + w[1:])
    return " ".join(out)


# --- note model ----------------------------------------------------------
@dataclass
class Note:
    title: str
    folder: str
    summary: str = ""
    source_ids: list = field(default_factory=list)
    aliases: list = field(default_factory=list)
    reviewed: bool = False
    generated_by: str = ""
    blocks: dict = field(default_factory=dict)     # source_id -> markdown block
    related: dict = field(default_factory=dict)    # title -> why
    sources: dict = field(default_factory=dict)    # source_id -> raw link line
    extra: str = ""                                # hand-written text we must keep

    @property
    def path(self):
        return config.WIKI_DIR / self.folder / f"{self.title}.md"

    def render(self):
        fm = ["---", f"title: {self.title}",
              f"aliases: [{', '.join(self.aliases)}]",
              f"type: {self.folder.lower().rstrip('s')}",
              f"source_ids: [{', '.join(self.source_ids)}]",
              f"generated_by: {self.generated_by}",
              f"reviewed: {'true' if self.reviewed else 'false'}",
              f"updated: {dt.date.today().isoformat()}", "---", ""]
        body = [f"# {self.title}", "", self.summary.strip(), "", "## Details", ""]
        for sid in self.source_ids:
            if sid in self.blocks:
                body += [f"<!-- src:{sid} -->", self.blocks[sid].strip(), f"<!-- /src:{sid} -->", ""]
        if self.extra.strip():
            body += [self.extra.strip(), ""]
        if self.related:
            body += ["## Related", ""]
            body += [f"- [[{t}]] — {why}" for t, why in sorted(self.related.items())]
            body.append("")
        body += ["## Sources", ""]
        body += [self.sources[s] for s in self.source_ids if s in self.sources]
        return "\n".join(fm + body).rstrip() + "\n"


def parse(path):
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    if text.startswith("---"):
        _, head, body = text.split("---", 2)
        for line in head.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    lst = lambda v: [x.strip() for x in v.strip("[]").split(",") if x.strip()]
    n = Note(title=fm.get("title", path.stem), folder=path.parent.name,
             source_ids=lst(fm.get("source_ids", "")), aliases=lst(fm.get("aliases", "")),
             reviewed=fm.get("reviewed") == "true", generated_by=fm.get("generated_by", ""))
    m = re.search(r"^# [^\n]*\n\n(.*?)\n\n## Details", body, re.S | re.M)
    n.summary = m.group(1).strip() if m else ""
    for sid, block in re.findall(r"<!-- src:(\S+) -->\n(.*?)\n<!-- /src:\1 -->", body, re.S):
        n.blocks[sid] = block
    rel = re.search(r"## Related\n\n(.*?)(\n## |\Z)", body, re.S)
    if rel:
        for t, why in re.findall(r"- \[\[([^\]]+)\]\] — (.*)", rel.group(1)):
            n.related[t] = why
    src = re.search(r"## Sources\n\n(.*)\Z", body, re.S)
    if src:
        for line in src.group(1).strip().splitlines():
            m2 = re.search(r"`([\w\-]+)`", line)
            if m2:
                n.sources[m2.group(1)] = line
    # keep any hand-written text between the last src block and ## Related
    det = re.search(r"## Details\n(.*?)(\n## Related|\n## Sources|\Z)", body, re.S)
    if det:
        n.extra = re.sub(r"<!-- src:(\S+) -->.*?<!-- /src:\1 -->", "", det.group(1), flags=re.S).strip()
    return n


def all_notes():
    return {p.stem.lower(): parse(p) for p in sorted(config.WIKI_DIR.rglob("*.md"))}


def find(notes, title):
    key = title.lower()
    if key in notes:
        return notes[key]
    for n in notes.values():
        if key in (a.lower() for a in n.aliases):
            return n
    return None


# --- link hygiene --------------------------------------------------------
def fix_links(log=print):
    """Drop [[links]] whose target doesn't exist (keeps the text). Returns count."""
    targets = {p.stem.lower() for p in config.VAULT.rglob("*.md")}
    targets |= {str(p.relative_to(config.VAULT).with_suffix("")).lower() for p in config.VAULT.rglob("*.md")}
    broken = 0
    for p in config.WIKI_DIR.rglob("*.md"):
        text = p.read_text(encoding="utf-8")

        def repl(m):
            nonlocal broken
            if m.group(1).strip().rstrip("\\").lower() in targets:
                return m.group(0)
            broken += 1
            log(f"  unlinked missing target [[{m.group(1)}]] in {p.name}")
            return (m.group(3) or "|" + m.group(1))[1:]
        new = WIKILINK.sub(repl, text)
        # a Related bullet whose link was removed is noise – drop the line
        out, in_related = [], False
        for line in new.splitlines():
            if line.startswith("## "):
                in_related = line == "## Related"
            if in_related and line.startswith("- ") and "[[" not in line:
                continue
            out.append(line)
        new = "\n".join(out) + "\n"
        if new != text:
            p.write_text(new, encoding="utf-8")
    return broken


def check_links():
    """Report (note, target) pairs that don't resolve. Used by `wiki check`."""
    targets = {p.stem.lower() for p in config.VAULT.rglob("*.md")}
    targets |= {str(p.relative_to(config.VAULT).with_suffix("")).lower() for p in config.VAULT.rglob("*.md")}
    bad = []
    for p in list(config.WIKI_DIR.rglob("*.md")) + [config.INDEX_MD, config.SOURCES_MD]:
        if p.exists():
            for m in WIKILINK.finditer(p.read_text(encoding="utf-8")):
                if m.group(1).strip().rstrip("\\").lower() not in targets:
                    bad.append((p.name, m.group(1)))
    return bad


# --- landing pages -------------------------------------------------------
def write_index(catalog):
    notes = sorted(all_notes().values(), key=lambda n: (n.folder, n.title))
    blurbs = {"Projects": "Things I built or ran, with results.",
              "Courses": "Assignment briefs and what each class asked for.",
              "Concepts": "Reusable ideas that show up across projects."}
    L = ["# Personal Wiki", "",
         "Course and project notes, generated from the originals in `raw/` by local Gemma and reviewed by hand.",
         "Start with a project, follow **Related** links to concepts, and use **Sources** at the bottom of any note to open the original evidence.",
         "", f"- [[Sources]] — catalog of the {len(catalog)} original documents and which notes they produced", ""]
    for folder in config.WIKI_FOLDERS:
        group = [n for n in notes if n.folder == folder]
        if not group:
            continue
        L += [f"## {folder}", "", f"_{blurbs.get(folder, '')}_", ""]
        for n in group:
            summ = n.summary.replace("\n", " ")
            first = summ if len(summ) <= 200 else re.split(r"(?<!\bMs\.)(?<!\bMr\.)(?<=\.)\s", summ, maxsplit=1)[0]
            L.append(f"- [[{n.title}]] — {first}")
        L.append("")
    config.INDEX_MD.write_text("\n".join(L), encoding="utf-8")


def write_sources_page(catalog):
    L = ["# Sources", "",
         "Original documents are kept **unchanged** in `raw/`. Machine IDs live here and in each note's `source_ids` property, never in filenames.",
         "", "| Source | ID | Original location | SHA-256 | Notes produced |", "|---|---|---|---|---|"]
    for sid, s in sorted(catalog.items()):
        stem = s["raw_path"].removesuffix(".md")
        notes = ", ".join(f"[[{t}]]" for t in s.get("notes", []))
        L.append(f"| [[{stem}\\|{s['title']}]] | `{sid}` | {s.get('origin', '—')} | `{s['sha256'][:12]}` | {notes} |")
    L += ["", "Back to [[index]]", ""]
    config.SOURCES_MD.write_text("\n".join(L), encoding="utf-8")


# --- cleanup -------------------------------------------------------------
def rename(old, new, log=print):
    """Rename a note: file, title, heading, incoming links, catalog. The old
    name becomes an alias so a later re-ingest updates this note instead of
    re-creating the machine-style name."""
    import json
    notes = all_notes()
    n = find(notes, old)
    if not n:
        raise FileNotFoundError(f"No note titled '{old}'")
    new = clean_title(new) or new
    if find(notes, new) and find(notes, new) is not n:
        raise RuntimeError(f"A note titled '{new}' already exists; merge by hand instead")
    old_path, old_title = n.path, n.title
    n.title = new
    if old_title not in n.aliases:
        n.aliases.append(old_title)
    n.path.write_text(n.render(), encoding="utf-8")
    old_path.unlink()
    pat = re.compile(r"\[\[" + re.escape(old_title) + r"(?=[\]|#])", re.I)
    touched = 0
    for p in config.VAULT.rglob("*.md"):
        if p.parts[-2] == "raw" or "raw" in p.relative_to(config.VAULT).parts[:1]:
            continue                                  # originals are never edited
        t = p.read_text(encoding="utf-8")
        t2 = pat.sub("[[" + new, t)
        if t2 != t:
            p.write_text(t2, encoding="utf-8")
            touched += 1
    if config.SOURCES_JSON.exists():
        cat = json.loads(config.SOURCES_JSON.read_text())
        for s in cat.values():
            s["notes"] = [new if x == old_title else x for x in s.get("notes", [])]
        config.SOURCES_JSON.write_text(json.dumps(cat, indent=2))
        write_index(cat)
        write_sources_page(cat)
    log(f"renamed [[{old_title}]] -> [[{new}]] ({touched} files with incoming links updated; old name kept as alias)")
