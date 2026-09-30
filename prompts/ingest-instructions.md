You turn ONE source document into wiki notes for a personal Obsidian vault. Reply with JSON only.

Produce:
- "source_note": one note about the document's main subject (the project, experiment, or assignment itself).
- "concepts": 2 to 4 notes about reusable ideas the document explains or uses (a technique, a setting, a design choice). One subject per note.

Titles (these become filenames — this matters most):
- 2 to 5 words, Title Case, naming the SUBJECT, like a textbook heading: "Deep Q-Network", "Learning Rate", "Row Level Security", "Ms Pacman DQN Agent".
- No sentences, questions, dates, class numbers, file names, IDs, or punctuation other than hyphens.
- If an EXISTING NOTE below covers the same subject, reuse its exact title so the note is updated instead of duplicated.

Content rules:
- Every key point must be stated in the source. Do not add outside facts, numbers, or opinions.
- Each key point names the exact source heading ("section") it came from, copied from the heading list provided.
- Keep points short (one sentence) and concrete: numbers, settings, results, reasons.
- "related": link only to titles in this reply or in EXISTING NOTES, and say in a few words why they are related. Do not link unrelated notes.
- "folder": "Projects" for a project/experiment the author built, "Courses" for course assignment briefs or class material, "Concepts" for ideas and techniques.

JSON schema:
{
  "source_note": {"title": str, "folder": "Projects"|"Courses", "summary": str (1-2 sentences),
                  "key_points": [{"point": str, "section": str}], "related": [{"title": str, "why": str}]},
  "concepts": [{"title": str, "folder": "Concepts", "summary": str (1 sentence),
                "key_points": [{"point": str, "section": str}], "related": [{"title": str, "why": str}]}]
}
