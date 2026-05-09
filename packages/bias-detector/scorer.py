from .lexicons import GENDERED_LANGUAGE, PRESTIGE_TERMS, AGE_INDICATORS

def score_bias(text: str):
    score = 0.0
    flags = []

    for word, label in GENDERED_LANGUAGE.items():
        if word in text:
            score += 0.3
            flags.append("gendered_language")

    for word, label in PRESTIGE_TERMS.items():
        if word in text:
            score += 0.4
            flags.append("prestige_bias")

    for phrase in AGE_INDICATORS:
        if phrase in text:
            score += 0.5
            flags.append("age_bias_risk")

    score = min(score, 1.0)

    return {
        "bias_score": round(score, 2),
        "flags": list(set(flags))
    }