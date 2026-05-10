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

    harm_score = (
        (gender_hits * 0.3) +
        (prestige_hits * 0.3) +
        (age_hits * 0.4)
    )

    sensitivity_score = (
        (race_hits * 0.2) +
        (disability_hits * 0.2)
    )

    harm_score = min(harm_score / 3, 1.0)
    sensitivity_score = min(sensitivity_score / 2, 1.0)

    total_score = min(harm_score + sensitivity_score, 1.0)

    if len(flags) >= 3:
        total_score *= 1.1
        total_score = min(total_score, 1.0)

    return {
        "bias_score": round(total_score, 2),
        "harm_score": round(harm_score, 2),
        "sensitivity_score": round(sensitivity_score, 2),
        "flags": list(flags)
    }