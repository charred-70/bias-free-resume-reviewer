from .lexicons import GENDERED_LANGUAGE, PRESTIGE_TERMS, AGE_INDICATORS

def score_bias(text: str):
    gender_score = 0.0
    prestige_score = 0.0
    age_score = 0.0
    flags = set()

    gender_hits = sum(1 for w in GENDERED_LANGUAGE if w in text)
    prestige_hits = sum(1 for w in PRESTIGE_TERMS if w in text)
    age_hits = sum(1 for w in AGE_INDICATORS if w in text)

    flags = set()

    if gender_hits:
        flags.add("gendered_language")
    if prestige_hits:
        flags.add("prestige_bias")
    if age_hits:
        flags.add("age_bias_risk")

    gender_score = (gender_hits / len(GENDERED_LANGUAGE)) * 0.5
    prestige_score = (prestige_hits / len(PRESTIGE_TERMS)) * 0.5
    age_score = (age_hits / len(AGE_INDICATORS)) * 0.6

    score = gender_score + prestige_score + age_score

    if len(flags) >= 2:
        score *= 1.2

    return {
        "bias_score": round(score, 2),
        "flags": list(flags)
    }