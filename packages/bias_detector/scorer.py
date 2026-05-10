from .lexicons import (
    GENDERED_LANGUAGE,
    PRESTIGE_TERMS,
    AGE_INDICATORS,
    RACE_INDICATORS,
    DISABILITY_INDICATORS
)


def score_bias(text: str):

    text = text.lower()

    flags = set()

    gender_hits = sum(1 for w in GENDERED_LANGUAGE if w in text)
    prestige_hits = sum(1 for w in PRESTIGE_TERMS if w in text)
    age_hits = sum(1 for w in AGE_INDICATORS if w in text)
    race_hits = sum(1 for w in RACE_INDICATORS if w in text)
    disability_hits = sum(1 for w in DISABILITY_INDICATORS if w in text)

    if gender_hits:
        flags.add("gendered_language")

    if prestige_hits:
        flags.add("prestige_bias")

    if age_hits:
        flags.add("age_bias_risk")

    if race_hits:
        flags.add("race_reference")

    if disability_hits:
        flags.add("disability_reference")

    gender_score = (gender_hits / len(GENDERED_LANGUAGE)) * 0.4
    prestige_score = (prestige_hits / len(PRESTIGE_TERMS)) * 0.4
    age_score = (age_hits / len(AGE_INDICATORS)) * 0.5

    race_score = (race_hits / len(RACE_INDICATORS)) * 0.2
    disability_score = (disability_hits / len(DISABILITY_INDICATORS)) * 0.2

    score = (
        gender_score +
        prestige_score +
        age_score +
        race_score +
        disability_score
    )
    if len(flags) >= 3:
        score *= 1.1

    return {
        "bias_score": round(min(score, 1.0), 2),
        "flags": list(flags)
    }