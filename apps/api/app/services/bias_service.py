from packages.bias_detector.scorer import score_bias
from apps.api.app.services.ml_bias_service import predict_bias
from packages.bias_detector.explainer import explain
from packages.nlp.sentence_splitter import split_sentences
from packages.nlp.sentence_risk import score_segments
from packages.bias_detector.rewrite_engine import rewrite_resume

# optional global model loader later
ml_model = None


def analyze_bias(cleaned_text: str):

    rule_result = score_bias(cleaned_text)

    ml_result = predict_bias(cleaned_text)

    rule_score = rule_result["bias_score"]
    harm_score = rule_result["harm_score"]
    sensitivity_score = rule_result["sensitivity_score"]
    ml_score = ml_result["bias_probability"]

    model_component = ml_score * 0.6
    harm_component = harm_score * 0.4

    sensitivity_penalty = 0.0
    if sensitivity_score > 0.7:
        sensitivity_penalty = 0.05

    final_score = model_component + harm_component + sensitivity_penalty
    final_score = min(final_score, 1.0)

    explanations = explain(cleaned_text, ml_score, rule_score)

    sentences = split_sentences(cleaned_text)

    sentence_map = score_segments(cleaned_text, ml_model=None)


    if final_score < 0.3:
        risk = "low"
    elif final_score < 0.7:
        risk = "medium"
    else:
        risk = "high"

    explanation_strength = (rule_score * 0.5) + (ml_score * 0.5)

    rewrites = rewrite_resume(cleaned_text)

    return {
        "bias_score": round(final_score, 2),
        "rule_score": round(rule_score, 2),
        "ml_score": round(ml_score, 2),
        "risk_level": risk,
        "flags": rule_result["flags"],
        "fairness_analysis": {
            "harm_score": harm_score,
            "sensitivity_score": sensitivity_score,
            "ml_score": ml_score
        },
        "model_type": "hybrid",
        "explanation": {
            "explanation_strength": round(explanation_strength, 2),
            "explanation": explanations,
            "sentence_risk_map": sentence_map
        },
        "rewrites": rewrites
    }