"""Chat mode = personal assistant with conversation memory and optional retrieval.

Each turn:
  system(persona.md) + last N messages + new user message  ->  Gemma with a
  `search_notes` tool. If Gemma calls the tool, the harness runs the retrieval
  tool, feeds the labeled passages back as a tool message, and asks Gemma again.
  If not, the reply is used directly. The harness prints which path was taken.
"""
import datetime as dt
import json
import re

from .. import citations, config, llm, prompts
from ..retrieval import Retriever, format_passages

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": "Search Laura's personal wiki (course and project notes) and return the most relevant "
                       "original passages with labels like [S1]. Use only when the answer depends on her notes.",
        "parameters": {"type": "object", "required": ["query"],
                       "properties": {"query": {"type": "string", "description": "keywords to search for"}}},
    },
}
HELP = """chat commands:
  /search <query>  force a notes search for this question
  /save            save the last reply to outputs/drafts/ (not evidence, not indexed)
  /clear           forget this conversation
  /help            this message
  /exit            quit"""


class ChatSession:
    def __init__(self, model=None, log_path=None, k=5):
        self.model = model or config.CHAT_MODEL
        self.system = prompts.load("persona.md")
        self.history = []            # user/assistant messages only
        self.retriever = None
        self.k = k
        self.last_reply = ""
        self.log_path = log_path

    def _retrieve(self, query):
        if self.retriever is None:
            self.retriever = Retriever()
        hits = self.retriever.search(query, k=self.k, scope="all")
        return hits, format_passages(hits)

    def turn(self, user_text, force_search=None):
        """Returns (reply, trace) where trace records whether retrieval happened."""
        window = self.history[-config.HISTORY_MESSAGES:]
        messages = [{"role": "system", "content": self.system}, *window,
                    {"role": "user", "content": user_text}]
        trace = {"searched": False, "query": None, "hits": [], "stats": []}

        if force_search:
            hits, block = self._retrieve(force_search)
            trace.update(searched=True, query=force_search, hits=hits, forced=True)
            messages[-1] = {"role": "user", "content":
                            f"{user_text}\n\n(Notes search results for '{force_search}':)\n{block}"}
            msg, stats = llm.chat(messages, model=self.model, temperature=0.6)
            trace["stats"].append(stats)
        else:
            msg, stats = llm.chat(messages, model=self.model, tools=[SEARCH_TOOL], temperature=0.6)
            trace["stats"].append(stats)
            calls = msg.get("tool_calls") or []
            if calls:
                args = calls[0]["function"].get("arguments") or {}
                if isinstance(args, str):
                    args = json.loads(args or "{}")
                query = args.get("query") or user_text
                hits, block = self._retrieve(query)
                trace.update(searched=True, query=query, hits=hits)
                messages += [msg, {"role": "tool", "tool_name": "search_notes",
                                   "content": block or "No matching passages."}]
                msg, stats = llm.chat(messages, model=self.model, temperature=0.6)
                trace["stats"].append(stats)

        reply = (msg.get("content") or "").strip()
        if trace["searched"]:
            trace["check"] = citations.check(reply, trace["hits"])
        self.history += [{"role": "user", "content": user_text}, {"role": "assistant", "content": reply}]
        self.last_reply = reply
        self._log(user_text, reply, trace)
        return reply, trace

    def _log(self, user_text, reply, trace):
        if not self.log_path:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a") as f:
            f.write(f"\n**you:** {user_text}\n\n")
            f.write(f"`{trace_line(trace)}`\n\n")
            f.write(f"**wren:** {reply}\n")
            if trace["searched"]:
                for h in trace["hits"]:
                    f.write(f"\n> [{h.label}] {h.chunk.location}")
                f.write("\n")

    def save_last(self):
        if not self.last_reply:
            return None
        config.DRAFTS.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = config.DRAFTS / f"draft-{stamp}.md"
        path.write_text("<!-- generated draft from chat; NOT source evidence -->\n\n" + self.last_reply + "\n")
        return path


def trace_line(trace):
    secs = sum(s["wall_s"] for s in trace["stats"])
    if not trace["searched"]:
        return f"· no notes searched · {secs:.1f}s"
    how = "forced /search" if trace.get("forced") else "Gemma called search_notes"
    return f'· {how}: "{trace["query"]}" → {len(trace["hits"])} passages · {secs:.1f}s'


def repl(model=None):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = config.EVIDENCE / "modes" / f"chat-{stamp}.md"
    s = ChatSession(model=model, log_path=log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(f"# Chat transcript {stamp}\n\nmode: chat · execution: local · model: `{s.model}`\n")
    print(f"Wren (chat) · model {s.model} · local · type /help for commands, /exit to quit")
    while True:
        try:
            text = input("\nyou › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text in ("/exit", "/quit"):
            break
        if text == "/help":
            print(HELP); continue
        if text == "/clear":
            s.history.clear(); print("(conversation cleared)"); continue
        if text == "/save":
            p = s.save_last(); print(f"(saved to {p})" if p else "(nothing to save yet)"); continue
        force = None
        m = re.match(r"/search\s+(.+)", text)
        if m:
            force = text = m.group(1)
        try:
            reply, trace = s.turn(text, force_search=force)
        except llm.ModelUnavailable as e:
            print(f"! {e}"); continue
        print(f"  {trace_line(trace)}")
        print(f"\nwren › {reply}")
        if trace["searched"]:
            print("\n" + citations.render(trace["check"]))
    print(f"(transcript saved to {log_path.relative_to(config.ROOT)})")
