"""Search mode: show original passages + locations. No language model involved."""
import textwrap

from ..retrieval import Retriever


def run(query, k=5, scope="all", show_full=False):
    r = Retriever()
    hits = r.search(query, k=k, scope=scope)
    lines = [f'search: "{query}"  (scope={scope}, top {k}, no answer generated)']
    if r.warning:
        lines.append(f"  ! {r.warning}")
    if not hits:
        lines.append("  no matching passages")
    for n, h in enumerate(hits, 1):
        c = h.chunk
        cos = "n/a" if h.cosine is None else f"{h.cosine:.3f}"
        tag = "ORIGINAL" if c.kind == "raw" else "wiki note (generated)"
        lines.append(f"\n[{n}] {c.location}  [{tag}]")
        lines.append(f"    bm25={h.bm25:.2f}  cosine={cos}  fused={h.score:.4f}")
        body = c.text if show_full else textwrap.shorten(c.text.replace("\n", " "), 420, placeholder=" …")
        lines.append(textwrap.indent(body, "    | "))
    return "\n".join(lines), hits
