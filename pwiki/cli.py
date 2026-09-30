"""wiki — personal wiki CLI (local Gemma via Ollama).

The CLI only parses arguments and picks a mode; the harness pieces live in
ingest.py, retrieval.py, modes/{search,ask,chat}.py, citations.py, evidence.py.
"""
import argparse
import json
import sys
import time

from . import config, llm

EPILOG = f"""
examples:
  wiki ingest vault/raw                     generate/update notes from every raw source
  wiki ingest "staging/New Notes.md"        copy one new source into vault/raw/ and ingest it
  wiki search "learning rate"               original passages + paths, no model answer
  wiki ask "What learning rate did I use?"  neutral, cited answer (or insufficient evidence)
  wiki chat                                 talk to Wren, the assistant (uses retrieval only when needed)
  wiki eval                                 run the 4 test questions, write evidence cards
  wiki check                                verify links and that notes/index are consistent

configuration (environment variables):
  WIKI_MODEL        chat model   (default {config.CHAT_MODEL})
  WIKI_EMBED_MODEL  embeddings   (default {config.EMBED_MODEL})
  OLLAMA_HOST       runtime URL  (default {config.OLLAMA_URL}; local only)

requires: Ollama running (`ollama serve`) with both models pulled once while online:
  ollama pull {config.CHAT_MODEL} && ollama pull {config.EMBED_MODEL}
"""


def main(argv=None):
    p = argparse.ArgumentParser(prog="wiki", description="Personal wiki over my course notes, "
                                "answered by a local Gemma model. Everything runs on this machine.",
                                epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default=None, help=f"Ollama model tag (default {config.CHAT_MODEL})")
    p.add_argument("--mode", choices=["local"], default="local",
                   help="where the model runs; only 'local' is implemented")
    sub = p.add_subparsers(dest="cmd", metavar="command")

    s = sub.add_parser("ingest", help="read sources, generate linked notes, update index")
    s.add_argument("path", nargs="?", default=str(config.RAW_DIR), help="file or folder (default vault/raw)")
    s.add_argument("--force", action="store_true", help="regenerate even if a source is unchanged")

    s = sub.add_parser("search", help="show matching original passages (no model answer)")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=5)
    s.add_argument("--scope", choices=["raw", "wiki", "all"], default="all")
    s.add_argument("--full", action="store_true", help="print whole passages")
    s.add_argument("--save", metavar="FILE", help="also write the output to FILE")

    s = sub.add_parser("ask", help="standalone factual answer with citations")
    s.add_argument("question")
    s.add_argument("--passages", action="store_true", help="list retrieved passages first")
    s.add_argument("--save", metavar="FILE", help="write a full evidence card to FILE")

    sub.add_parser("chat", help="talk with Wren, the assistant (conversation + optional retrieval)")
    s = sub.add_parser("eval", help="run evals/questions.json in ask mode, save evidence cards")
    s.add_argument("--only", help="run one test id, e.g. test2")
    s.add_argument("--out", default=str(config.EVIDENCE / "ask"))
    sub.add_parser("check", help="check wiki links, filenames, and index")
    s = sub.add_parser("rename", help="rename a note and update every link to it")
    s.add_argument("old")
    s.add_argument("new")
    sub.add_parser("reindex", help="rebuild the retrieval index only")
    sub.add_parser("help", help="show this help")

    a = p.parse_args(argv)
    if a.cmd in (None, "help"):
        p.print_help()
        return 0
    try:
        return _dispatch(a)
    except llm.ModelUnavailable as e:
        print(f"error: local model unavailable — {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


def _dispatch(a):
    from pathlib import Path
    if a.cmd == "ingest":
        from . import ingest
        t0 = time.perf_counter()
        ingest.run(a.path, force=a.force, model=a.model)
        print(f"done in {time.perf_counter() - t0:.1f}s")
    elif a.cmd == "search":
        from .modes import search
        out, _ = search.run(a.query, k=a.k, scope=a.scope, show_full=a.full)
        print(out)
        if a.save:
            from . import evidence
            evidence.save(Path(a.save), f"# wiki search\n\n```text\n$ wiki search \"{a.query}\"\n{out}\n```\n")
    elif a.cmd == "ask":
        from .modes import ask
        rec = ask.run(a.question, model=a.model)
        print(ask.render(rec, show_passages=a.passages))
        if a.save:
            from . import evidence
            print(f"(evidence card: {evidence.save(Path(a.save), evidence.ask_card(rec))})")
    elif a.cmd == "chat":
        from .modes import chat
        chat.repl(model=a.model)
    elif a.cmd == "eval":
        from . import evidence
        from .modes import ask
        tests = json.loads(config.EVALS.read_text())["tests"]
        for t in tests:
            if a.only and t["id"] != a.only:
                continue
            print(f"\n=== {t['id']} ({t['kind']}): {t['question']}")
            t0 = time.perf_counter()
            rec = ask.run(t["question"], model=a.model)
            print(ask.render(rec, show_passages=True))
            print(f"(end-to-end {time.perf_counter() - t0:.1f}s incl. retrieval)")
            path = evidence.save(Path(a.out) / f"{t['id']}.md", evidence.ask_card(rec, t))
            print(f"(evidence card: {path})")
    elif a.cmd == "check":
        from . import notes
        bad = notes.check_links()
        names = [p.stem for p in config.WIKI_DIR.rglob("*.md")]
        weird = [n for n in names if not notes.clean_title(n)]
        dupes = {n for n in names if [x.lower() for x in names].count(n.lower()) > 1}
        heading_mismatch = [p.name for p in config.WIKI_DIR.rglob("*.md")
                            if f"\n# {p.stem}\n" not in p.read_text(encoding="utf-8")]
        print(f"{len(names)} notes · {len(bad)} broken links · {len(weird)} machine-style names · "
              f"{len(dupes)} duplicate titles · {len(heading_mismatch)} heading/filename mismatches")
        for x in bad:
            print(f"  broken: {x[0]} -> [[{x[1]}]]")
        for x in weird + sorted(dupes) + heading_mismatch:
            print(f"  problem: {x}")
        return 1 if (bad or weird or dupes or heading_mismatch) else 0
    elif a.cmd == "rename":
        from . import index, notes
        notes.rename(a.old, a.new)
        index.build()
    elif a.cmd == "reindex":
        from . import index
        index.build(force=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
