import re

SECTION_KEYWORDS = {
    "education": ["education"],
    "experience": ["experience", "work experience", "internship"],
    "projects": ["projects"],
    "skills": ["skills", "technical skills"],
}


def segment_resume(text: str):

    text = text.lower()

    sections = {}
    current = "header"
    sections[current] = []

    words = text.split()

    for word in words:

        matched_section = None

        for section, keywords in SECTION_KEYWORDS.items():
            if any(k in word for k in keywords):
                matched_section = section
                break

        if matched_section:
            current = matched_section
            sections.setdefault(current, [])
            continue

        sections.setdefault(current, []).append(word)

    # join words back into strings
    return {
        k: " ".join(v).strip()
        for k, v in sections.items()
    }