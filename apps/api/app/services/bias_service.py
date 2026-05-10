from packages.bias_detector.scorer import score_bias
from apps.api.app.services.ml_bias_service import predict_bias

# optional global model loader later
ml_model = None


def analyze_bias(cleaned_text: str):

    rule_result = score_bias(cleaned_text)

    ml_result = predict_bias(cleaned_text)

    rule_score = rule_result["bias_score"]
    ml_score = ml_result["bias_probability"]

    final_score = (rule_score * 0.4) + (ml_score * 0.6)

    if final_score < 0.3:
        risk = "low"
    elif final_score < 0.7:
        risk = "medium"
    else:
        risk = "high"

    return {
        "bias_score": round(final_score, 2),
        "rule_score": round(rule_score, 2),
        "ml_score": round(ml_score, 2),
        "risk_level": risk,
        "flags": rule_result["flags"],
        "model_type": "hybrid"
    }