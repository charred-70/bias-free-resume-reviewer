from .rewrite_config import REWRITE_RULES
from .suggestion_builder import build_suggestions
from packages.ml_core.generation.rewrite_generator import rewrite_with_transformer

def rewrite_resume(text: str):

    rewritten = text

    suggestions = []

    for old, new in REWRITE_RULES.items():

        if old in rewritten:

            rewritten = rewritten.replace(old, new)

            suggestions.append({
                "original": old,
                "replacement": new
            })

    try:
        ml_rewrite = rewrite_with_transformer(text)

        suggestions = build_suggestions(text, ml_rewrite)

        return {
            "rewritten_text": ml_rewrite,
            "suggestions": suggestions + [{
                "original": "full_text",
                "replacement": "ml_rewrite",
                "reason": "transformer rewrite"
            }],
            "rewrite_strength": 0.9
        }

    except Exception:
        return {
            "rewritten_text": rewritten,
            "suggestions": suggestions,
            "rewrite_strength": 0.5
        }