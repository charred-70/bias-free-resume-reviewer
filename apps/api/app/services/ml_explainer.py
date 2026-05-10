def explain_ml(ml_score, rule_score):

    return {
        "ml_contribution": round(ml_score * 0.6, 2),
        "rule_contribution": round(rule_score * 0.4, 2)
    }