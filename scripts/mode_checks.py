"""Chat/search/ask mode-boundary checks, written to one Markdown transcript.

Uses the exact same ChatSession, search, and ask code as the interactive CLI;
this script only supplies the user's lines so the run is repeatable.
"""
import argparse
import datetime as dt
from pathlib import Path

from pwiki import config, evidence, llm
from pwiki.modes import ask, chat, search

CHAT_TURNS = [
    ("capabilities", "what can you help me with?", "explain real capabilities; no notes search, no citations, no refusal"),
    ("capabilities", "what can we do?", "same: conversational, no notes search"),
    ("draft", "Draft a 5-step study plan for reviewing my Pac-Man DQN project before a quiz.",
     "may search notes; any facts about the project must carry [S#] citations; plan labeled as suggestion"),
    ("follow-up", "make that shorter", "rewrite the previous plan using conversation context; no new search"),
    ("chat-only claim", "Fun fact: my favorite ghost in the Pac-Man project was Sue.",
     "acknowledge; must not treat this as a verified note"),
]
CHAT_ONLY_Q = "What was my favorite ghost in the Pac-Man project?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(config.EVIDENCE / "modes" / "mode-checks.md"))
    a = ap.parse_args()
    info = llm.model_info()
    L = [f"# Mode boundary checks — {dt.datetime.now():%Y-%m-%d %H:%M}", "",
         f"- model: `{info['model']}` · {info.get('quantization')} · digest `{info.get('digest')}` · execution **local** (Ollama {info.get('ollama_version')})",
         f"- network: {evidence.internet_status()}",
         f"- device: {evidence.device_line()}", ""]

    L += ["## 1. Chat (one continuous conversation with Wren)", ""]
    s = chat.ChatSession()
    for kind, text, expect in CHAT_TURNS:
        reply, trace = s.turn(text)
        line = chat.trace_line(trace)
        print(f"you › {text}\n  {line}\nwren › {reply}\n")
        L += [f"### {kind}: “{text}”", "", f"_Expected:_ {expect}", "",
              f"**Harness trace:** `{line}`", "", "```text", reply, "```", ""]
        if trace["searched"]:
            L += [f"- [{h.label}] {h.chunk.location}" for h in trace["hits"]]
            chk = trace["check"]
            L += [f"- citation check: {'ok' if chk['ok'] else '; '.join(chk['problems'])} (cited: {', '.join(chk['cited']) or 'none'})", ""]

    L += ["## 2. Search (retrieval tool only, no model answer)", ""]
    out, _ = search.run("exploration rate Pac-Man", k=3, scope="raw")
    print(out)
    L += ["```text", f'$ wiki search "exploration rate Pac-Man" --scope raw -k 3', out, "```", ""]

    L += ["## 3. Ask ignores chat history", "",
          f"The chat above claimed a favorite ghost. Ask mode starts fresh and only sees retrieved raw passages:", ""]
    rec = ask.run(CHAT_ONLY_Q)
    rendered = ask.render(rec, show_passages=True)
    print(rendered)
    L += ["```text", f'$ wiki ask "{CHAT_ONLY_Q}"', rendered, "```", "",
          "_Expected:_ INSUFFICIENT EVIDENCE — the claim exists only in chat, not in any source.", ""]
    L += ["## Assessment (human review)", "", "_TODO_", ""]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(L), encoding="utf-8")
    print(f"(saved {a.out})")


if __name__ == "__main__":
    main()
