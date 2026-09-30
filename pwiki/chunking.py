"""Split Markdown into passages that keep their source path, heading, and lines.

Strategy: cut at headings first (sections are natural units), then split long
sections into ~CHUNK_WORDS-word windows with CHUNK_OVERLAP words of overlap,
breaking on line boundaries so tables and bullets stay intact.
"""
import re
from dataclasses import dataclass, asdict

from . import config

HEADING = re.compile(r"^(#{1,6})\s+(.*)")
FRONTMATTER_END = re.compile(r"^---\s*$")


@dataclass
class Chunk:
    id: str          # "<relpath>#<n>" – stable as long as the file is unchanged
    path: str        # path relative to vault/, e.g. "raw/Class 3 - Ms Pacman DQN.md"
    kind: str        # "raw" (original evidence) or "wiki" (generated note)
    heading: str     # "Parent > Child" heading trail
    line_start: int  # 1-based, inclusive
    line_end: int
    text: str

    def to_dict(self):
        return asdict(self)

    @property
    def location(self):
        return f"{self.path} § {self.heading} (L{self.line_start}-{self.line_end})"


def _sections(lines):
    """Yield (heading_trail, [(lineno, text), ...]) for each heading section."""
    trail, body = [], []
    in_code = False
    start = 0
    # skip YAML frontmatter (wiki notes) – it's metadata, not content
    if lines and FRONTMATTER_END.match(lines[0]):
        for i in range(1, len(lines)):
            if FRONTMATTER_END.match(lines[i]):
                start = i + 1
                break
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING.match(line)
        if m:
            if body:
                yield " > ".join(t for _, t in trail) or "(top)", body
            level = len(m.group(1))
            trail = [(lvl, t) for lvl, t in trail if lvl < level] + [(level, m.group(2).strip())]
            body = [(i + 1, line)]
        else:
            body.append((i + 1, line))
    if body:
        yield " > ".join(t for _, t in trail) or "(top)", body


def chunk_file(path, rel_path, kind):
    lines = path.read_text(encoding="utf-8").splitlines()
    chunks = []
    for heading, body in _sections(lines):
        window, words = [], 0
        for lineno, line in body:
            window.append((lineno, line))
            words += len(line.split())
            if words >= config.CHUNK_WORDS:
                chunks.append(_make(rel_path, kind, heading, window, len(chunks)))
                # carry trailing lines worth ~CHUNK_OVERLAP words into the next window
                keep, kept_words = [], 0
                for item in reversed(window):
                    if kept_words >= config.CHUNK_OVERLAP:
                        break
                    keep.insert(0, item)
                    kept_words += len(item[1].split())
                window, words = keep, kept_words
        if any(l.strip() for _, l in window) and (not chunks or window[-1][0] > chunks[-1].line_end):
            chunks.append(_make(rel_path, kind, heading, window, len(chunks)))
    # drop passages that are only a heading or whitespace
    return [c for c in chunks if len(c.text.split()) > 3]


def _make(rel_path, kind, heading, window, n):
    text = "\n".join(l for _, l in window).strip()
    return Chunk(f"{rel_path}#{n}", rel_path, kind, heading, window[0][0], window[-1][0], text)
