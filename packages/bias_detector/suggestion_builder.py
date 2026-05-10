import difflib


def build_suggestions(original: str, rewritten: str):

    original_sentences = original.split(".")
    rewritten_sentences = rewritten.split(".")

    diff = difflib.SequenceMatcher(
        None,
        original_sentences,
        rewritten_sentences
    )

    suggestions = []

    for tag, i1, i2, j1, j2 in diff.get_opcodes():

        if tag == "replace":
            suggestions.append({
                "original": " ".join(original_sentences[i1:i2]),
                "replacement": " ".join(rewritten_sentences[j1:j2]),
                "reason": "ML rewrite adjustment"
            })

        elif tag == "delete":
            suggestions.append({
                "original": " ".join(original_sentences[i1:i2]),
                "replacement": "",
                "reason": "removed bias-related content"
            })

        elif tag == "insert":
            suggestions.append({
                "original": "",
                "replacement": " ".join(rewritten_sentences[j1:j2]),
                "reason": "added clarification / neutrality"
            })

    return suggestions