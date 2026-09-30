"""Build and load the local retrieval index (stored in data/index/, outside the vault).

Files:
  chunks.jsonl    one passage per line (text + path + heading + line range)
  embeddings.npy  float32 [n_chunks, dim], L2-normalised, from embeddinggemma
  meta.json       file hashes + embed model, so we only rebuild when something changed
"""
import hashlib
import json

import numpy as np

from . import config, llm
from .chunking import Chunk, chunk_file

CHUNKS = config.INDEX_DIR / "chunks.jsonl"
EMBEDS = config.INDEX_DIR / "embeddings.npy"
META = config.INDEX_DIR / "meta.json"


def _indexed_files():
    """Raw originals + wiki notes. index.md/Sources.md are navigation, not content."""
    files = [(p, "raw") for p in sorted(config.RAW_DIR.rglob("*.md"))]
    files += [(p, "wiki") for p in sorted(config.WIKI_DIR.rglob("*.md"))]
    return files


def _fingerprint(files):
    h = {}
    for p, _ in files:
        h[str(p.relative_to(config.VAULT))] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    return h


def build(force=False, log=print):
    files = _indexed_files()
    fp = _fingerprint(files)
    if not force and META.exists():
        meta = json.loads(META.read_text())
        if meta.get("files") == fp and meta.get("embed_model") == config.EMBED_MODEL:
            log(f"  index up to date ({meta['n_chunks']} passages)")
            return
    chunks = []
    for p, kind in files:
        chunks.extend(chunk_file(p, str(p.relative_to(config.VAULT)), kind))
    config.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with CHUNKS.open("w") as f:
        for c in chunks:
            f.write(json.dumps(c.to_dict()) + "\n")
    # Embed "heading + text" so section titles help matching.
    vecs = np.array(llm.embed([f"{c.heading}\n{c.text}" for c in chunks]), dtype=np.float32)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9
    np.save(EMBEDS, vecs)
    META.write_text(json.dumps(
        {"files": fp, "embed_model": config.EMBED_MODEL, "n_chunks": len(chunks)}, indent=2))
    n_raw = sum(c.kind == "raw" for c in chunks)
    log(f"  indexed {len(chunks)} passages ({n_raw} raw, {len(chunks) - n_raw} wiki) "
        f"from {len(files)} files")


def load():
    if not CHUNKS.exists():
        raise FileNotFoundError("No index yet. Run: wiki ingest vault/raw  (or: wiki reindex)")
    chunks = [Chunk(**json.loads(l)) for l in CHUNKS.read_text().splitlines()]
    vecs = np.load(EMBEDS) if EMBEDS.exists() else None
    return chunks, vecs
