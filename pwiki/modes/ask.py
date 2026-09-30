"""Ask mode = the RAG workflow.

question -> retrieve raw passages -> label S1..Sn -> research rules + passages
-> local Gemma -> citation check -> answer + sources.
Stateless by design: no chat history, no persona, temperature 0.
"""
import re

from .. import citations, config, llm, prompts
from ..retrieval import Retriever, format_passages


def run(question, k=config.TOP_K, model=None):
    r = Retriever()
    hits = r.expand(r.search(question, k=k, scope="raw"))   # original evidence only, never drafts
    record = {"mode": "ask", "question": question, "hits": hits,
              "retrieval_warning": r.warning, "model": model or config.CHAT_MODEL}

    # Gate: nothing lexically or semantically close -> don't let the model improvise.
    best_cos = max((h.cosine for h in hits if h.cosine is not None), default=None)
    if not hits or (best_cos is not None and best_cos < config.MIN_COSINE
                    and max(h.bm25 for h in hits) == 0):
        record.update(answer=f"{citations.INSUFFICIENT}: no passage in the notes matches this question.",
                      gated=True, stats={}, check=citations.check(citations.INSUFFICIENT, []))
        return record

    block = format_passages(hits)
    messages = prompts.ask_messages(question, block)
    msg, stats = llm.chat(messages, model=model, temperature=0.0)
    # Gemma sometimes wraps numbers in LaTeX ($0.001$) despite the plain-text rule
    answer = re.sub(r"\$([0-9][0-9.,%]*)\$", r"\1", msg.get("content", "").strip())
    record.update(answer=answer, gated=False, stats=stats, prompt=messages,
                  check=citations.check(answer, hits))
    return record


def render(record, show_passages=False):
    out = []
    if record.get("retrieval_warning"):
        out.append(f"! {record['retrieval_warning']}")
    if show_passages:
        out.append("Retrieved passages:")
        for h in record["hits"]:
            out.append(f"  [{h.label or '-'}] {h.chunk.location}")
        out.append("")
    out.append(record["answer"])
    out.append("")
    out.append(citations.render(record["check"]))
    s = record.get("stats") or {}
    tail = f"model: {record['model']} (local)"
    if s:
        tail += f" · {s['wall_s']}s · {s['prompt_tokens']} prompt tok · {s['output_tokens']} out tok"
    elif record.get("gated"):
        tail += " · model not called (retrieval gate)"
    out.append(tail)
    return "\n".join(out)
