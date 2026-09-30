"""The retrieval tool: find evidence passages. It never calls the chat model.

Hybrid scoring:
  1. BM25 over word tokens (exact terms like "0.001", "DQN", "learning rate")
  2. cosine similarity with embeddinggemma vectors (paraphrases)
  3. reciprocal-rank fusion (RRF) combines the two rankings without having to
     calibrate their very different score scales.
If the embedding model is unreachable, search degrades to BM25 only and says so.
"""
import math
import re
from collections import Counter
from dataclasses import dataclass

import numpy as np

from . import config, index, llm
from .chunking import Chunk

TOKEN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")
STOP = set("""a an and are as at be by did do does for from how i in is it my of on or
that the this to was were what when where which who why with you your me""".split())


def _stem(t):
    # light plural folding so "rates" matches "rate" (v1 missed this)
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss") and not t[-2].isdigit():
        return t[:-1]
    return t


def tokenize(text):
    words = [_stem(t) for t in TOKEN.findall(text.lower()) if t not in STOP]
    # add bigrams so an exact phrase ("learning rate") outweighs its common words
    return words + [a + "_" + b for a, b in zip(words, words[1:])]


@dataclass
class Hit:
    chunk: object
    score: float        # fused RRF score (ranking only)
    bm25: float
    cosine: float | None
    label: str = ""     # "S1".. assigned by the caller that shows it to Gemma


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.tfs = [Counter(d) for d in docs]
        self.lens = [len(d) for d in docs]
        self.avg = sum(self.lens) / max(len(docs), 1)
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query_tokens):
        out = []
        for tf, dl in zip(self.tfs, self.lens):
            s = 0.0
            for t in query_tokens:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg))
            out.append(s)
        return out


class Retriever:
    def __init__(self):
        self.chunks, self.vecs = index.load()
        self.bm25 = BM25([tokenize(c.heading + " " + c.text) for c in self.chunks])
        self.embeddings_ok = self.vecs is not None
        self.warning = None

    def search(self, query, k=config.TOP_K, scope="all"):
        allowed = [i for i, c in enumerate(self.chunks) if scope == "all" or c.kind == scope]
        bm = self.bm25.scores(tokenize(query))
        cos = None
        if self.embeddings_ok:
            try:
                q = np.array(llm.embed([query])[0], dtype=np.float32)
                q /= np.linalg.norm(q) + 1e-9
                cos = self.vecs @ q
            except llm.ModelUnavailable as e:
                self.warning = f"embeddings unavailable, keyword-only search ({e})"
                self.embeddings_ok = False
        fused = {i: 0.0 for i in allowed}
        for i, r in _ranks(allowed, bm, positive_only=True).items():
            fused[i] += 1 / (config.RRF_K + r)
        if cos is not None:
            for i, r in _ranks(allowed, cos).items():
                fused[i] += 1 / (config.RRF_K + r)
        ranked = sorted(allowed, key=lambda i: fused[i], reverse=True)
        top = _diversify(ranked, self.chunks, k)
        return [Hit(self.chunks[i], fused[i], bm[i], None if cos is None else float(cos[i]))
                for i in top if fused[i] > 0]


    def expand(self, hits, top_n=config.EXPAND_TOP):
        """Ask-mode fix (test2 v1): a passage cut at a chunk boundary lost the
        rest of its section. For the best `top_n` hits, extend the passage
        through the next chunk of the SAME section, re-reading the original
        lines so the overlap isn't duplicated."""
        by_id = {c.id: i for i, c in enumerate(self.chunks)}
        shown = {h.chunk.id for h in hits}
        for h in hits[:top_n]:
            i = by_id[h.chunk.id]
            nxt = self.chunks[i + 1] if i + 1 < len(self.chunks) else None
            if not nxt or nxt.path != h.chunk.path or nxt.heading != h.chunk.heading or nxt.id in shown:
                continue
            lines = (config.VAULT / h.chunk.path).read_text(encoding="utf-8").splitlines()
            c = h.chunk
            h.chunk = Chunk(c.id, c.path, c.kind, c.heading, c.line_start, nxt.line_end,
                            "\n".join(lines[c.line_start - 1:nxt.line_end]).strip())
            shown.add(nxt.id)
        return hits


def _diversify(ranked, chunks, k, per_source=config.MAX_PER_SOURCE):
    """Take the best k, but at most `per_source` from one file (v1 fix: a
    two-source question returned 5/5 passages from one README)."""
    top, count = [], {}
    for i in ranked:
        p = chunks[i].path
        if count.get(p, 0) < per_source:
            top.append(i)
            count[p] = count.get(p, 0) + 1
        if len(top) == k:
            break
    return top


def _ranks(ids, scores, positive_only=False):
    ordered = sorted((i for i in ids if not positive_only or scores[i] > 0),
                     key=lambda i: scores[i], reverse=True)
    return {i: r + 1 for r, i in enumerate(ordered)}


def format_passages(hits):
    """Label passages S1..Sn and render them for a prompt. Mutates hit.label."""
    blocks = []
    for n, h in enumerate(hits, 1):
        h.label = f"S{n}"
        c = h.chunk
        blocks.append(f"[{h.label}] source: {c.path} | section: {c.heading} | "
                      f"lines {c.line_start}-{c.line_end}\n{c.text}")
    return "\n\n".join(blocks)
