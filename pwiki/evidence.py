"""Save what actually happened, so a reader can inspect runs without rerunning."""
import datetime as dt
import json
import platform
import subprocess

from . import config, llm


def device_line():
    try:
        chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                              capture_output=True, text=True).stdout.strip()
        mem = int(subprocess.run(["sysctl", "-n", "hw.memsize"],
                                 capture_output=True, text=True).stdout) / 2**30
        return f"{chip}, {mem:.0f} GB unified memory, macOS {platform.mac_ver()[0]}"
    except Exception:
        return platform.platform()


def internet_status():
    """Record whether the machine could reach the internet at run time."""
    import socket
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=2).close()
        return "ONLINE (internet reachable)"
    except OSError:
        return "OFFLINE (internet unreachable)"


def ask_card(record, test=None):
    """Markdown evidence card for one ask-mode run."""
    info = llm.model_info(record["model"])
    now = dt.datetime.now().isoformat(timespec="seconds")
    title = f"{test['id']}: {test['kind']}" if test else "ask run"
    L = [f"# Evidence card — {title}", "",
         "| field | value |", "|---|---|",
         f"| run at | {now} |",
         f"| interaction mode | **ask** (stateless, no chat history, no persona) |",
         f"| execution | **local** — Ollama {info.get('ollama_version', '?')} on 127.0.0.1 |",
         f"| network | {internet_status()} |",
         f"| model | `{info['model']}` · {info.get('parameter_size')} · {info.get('quantization')} · digest `{info.get('digest')}` |",
         f"| embeddings | `{config.EMBED_MODEL}` (local) + BM25, RRF fusion, top {len(record['hits'])} raw passages |",
         f"| device | {device_line()} |", ""]
    L += ["## Question", "", f"> {record['question']}", ""]
    if test:
        L += ["## Expected (written before the run, from `evals/questions.json`)", "",
              f"- **Behavior:** {test['expected_behavior']}",
              f"- **Sources:** {', '.join(test['expected_sources']) or '(none — unsupported question)'}",
              f"- **Passage:** {test['expected_passage'] or '—'}", ""]
    L += ["## Retrieved passages (exactly what Gemma saw)", ""]
    if record.get("retrieval_warning"):
        L.append(f"> ⚠️ {record['retrieval_warning']}\n")
    for h in record["hits"]:
        c = h.chunk
        cos = "n/a" if h.cosine is None else f"{h.cosine:.3f}"
        L += [f"<details><summary><b>[{h.label}]</b> {c.location} — bm25 {h.bm25:.2f}, cosine {cos}</summary>",
              "", "```text", c.text, "```", "</details>", ""]
    L += ["## Gemma's answer (verbatim)", "", "```text", record["answer"], "```", ""]
    chk = record["check"]
    L += ["## Automatic citation check", ""]
    L += [f"- [{s['label']}] → `{s['location']}`" for s in chk["sources"]] or ["- (no citations)"]
    L += [f"- insufficient-evidence response: **{'yes' if chk['insufficient'] else 'no'}**",
          f"- all citations point to retrieved passages: **{'yes' if not chk['invalid'] else 'NO'}**"]
    L += [f"- ⚠️ {p}" for p in chk["problems"]]
    s = record.get("stats") or {}
    if s:
        L += ["", "## Timing", "",
              f"- wall time {s['wall_s']} s (model load {s['load_s']} s) · "
              f"{s['prompt_tokens']} prompt tokens · {s['output_tokens']} output tokens · "
              f"{s['tokens_per_s']} tok/s",
              f"- loaded model memory (ollama ps): {llm.loaded_memory()}"]
    L += ["", "## Assessment (human review)", "", "_TODO: open each cited passage and verify every claim._", ""]
    return "\n".join(L)


def save(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def append_jsonl(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(obj, default=str) + "\n")
