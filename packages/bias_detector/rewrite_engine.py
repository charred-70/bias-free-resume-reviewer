from .rewrite_config import REWRITE_RULES
from .rewrite_schema import RewriteResult

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

    return {
        "rewritten_text": rewritten,
        "suggestions": suggestions
    }