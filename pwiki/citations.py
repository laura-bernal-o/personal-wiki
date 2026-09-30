"""Check that the model's [S#] citations point at passages we actually sent.

A citation is only a pointer. This module catches pointers to nothing (invented
labels) and answers with no citations. Whether the cited passage really
supports the claim is checked by a human in each evidence card.
"""
import re

CITE = re.compile(r"\[(S\d+)\]")
INSUFFICIENT = "INSUFFICIENT EVIDENCE"


def check(answer, hits):
    labels = {h.label: h for h in hits}
    cited = list(dict.fromkeys(CITE.findall(answer)))   # unique, in order
    valid = [c for c in cited if c in labels]
    invalid = [c for c in cited if c not in labels]
    insufficient = answer.strip().upper().startswith(INSUFFICIENT)
    problems = []
    if invalid:
        problems.append(f"cites passages that were not provided: {', '.join(invalid)}")
    if not insufficient and not valid:
        problems.append("answer makes claims without any citation")
    return {
        "insufficient": insufficient,
        "cited": valid,
        "invalid": invalid,
        "sources": [{"label": c, "location": labels[c].chunk.location} for c in valid],
        "ok": not problems,
        "problems": problems,
    }


def render(result):
    lines = []
    if result["sources"]:
        lines.append("Sources:")
        lines += [f"  [{s['label']}] {s['location']}" for s in result["sources"]]
    for p in result["problems"]:
        lines.append(f"  ! citation check: {p}")
    if result["ok"]:
        lines.append("  citation check: all citations point to retrieved passages")
    return "\n".join(lines)
