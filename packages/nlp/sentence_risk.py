def split_sentences(text: str):
    return text.split(".")

def score_segments(sentences, ml_score, rule_score):

    results = []

    for s in sentences:
        s_clean = s.strip()

        if not s_clean:
            continue

        local_risk = 0.0

        if "aggressive" in s_clean.lower():
            local_risk += 0.3

        if "google" in s_clean.lower():
            local_risk += 0.3

        if "years" in s_clean.lower():
            local_risk += 0.2

        combined = (local_risk * 0.6) + (ml_score * 0.3) + (rule_score * 0.1)

        results.append({
            "segment": s_clean,
            "risk": round(min(combined, 1.0), 2)
        })

    return results