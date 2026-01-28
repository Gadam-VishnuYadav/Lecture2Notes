"""
semantic_cleaner.py
Cleans filler words and broken sentences.
DOES NOT remove any language text.
"""

import re


def semantic_clean(text: str) -> str:
    # If transcript is empty
    if not text.strip():
        return ""

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned = []

    for s in sentences:
        # Skip very short sentences
        if len(s.split()) < 4:
            continue

        # Remove filler / hesitation words (multi-language safe)
        s = re.sub(
            r"\b(uh|um|ah|er|basically|actually|ante|matlab|hmm)\b",
            "",
            s,
            flags=re.IGNORECASE
        )

        s = re.sub(r"\s+", " ", s).strip()

        # Ensure proper sentence ending
        if s and s[-1] not in ".!?":
            s += "."

        cleaned.append(s)

    return " ".join(cleaned)
