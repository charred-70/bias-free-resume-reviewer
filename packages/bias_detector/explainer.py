from .explainer_config import EXPLANATION_TEMPLATES, CATEGORIES
def detect_categories(text: str):

    text = text.lower()

    categories = []

    if any(x in text for x in ["harvard", "google", "microsoft", "stanford"]):
        categories.append("prestige")

    if "years experience" in text or "10 years" in text:
        categories.append("experience_intensity")

    if any(x in text for x in ["aggressive", "passionate", "driven"]):
        categories.append("tone")

    return categories

def explain(text: str, ml_score: float, rule_score: float):

    categories = detect_categories(text)

    explanations = [
        EXPLANATION_TEMPLATES.get(c, "Unknown bias pattern detected")
        for c in categories
    ]

    # ML-aware generic explanation (NO text dependency)
    if ml_score > 0.8:
        explanations.append("Model detected strong bias-related semantic patterns")
    elif ml_score > 0.5:
        explanations.append("Model detected moderate bias-related patterns")

    return {
        "top_reasons": explanations,
        "categories_detected": categories,
        "ml_context": {
            "ml_strength": ml_score
        }
    }