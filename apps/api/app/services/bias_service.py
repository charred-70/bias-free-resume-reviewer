from packages.bias_detector.scorer import score_bias

def analyze_bias(cleaned_text: str):
    result = score_bias(cleaned_text)

    bias_score = result["bias_score"]

    if bias_score < 0.3:
        risk = "low"
    elif bias_score < 0.7:
        risk = "medium"
    else:
        risk = "high"

    return {
        "bias_score": bias_score,
        "risk_level": risk,
        "flags": result["flags"]
    }