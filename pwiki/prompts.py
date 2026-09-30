"""Load instruction files. Gemma never reads these on its own: the harness
puts the right file into the system message for each mode."""
from . import config


def load(name):
    path = config.PROMPTS / name
    if not path.exists():
        raise FileNotFoundError(f"Missing instruction file: {path}")
    return path.read_text(encoding="utf-8").strip()


def ask_messages(question, passages_block):
    """Ask mode: research rules + evidence + question. No persona, no history."""
    return [
        {"role": "system", "content": load("wiki-instructions.md")},
        {"role": "user", "content": f"SOURCE PASSAGES:\n\n{passages_block}\n\nQUESTION: {question}"},
    ]
