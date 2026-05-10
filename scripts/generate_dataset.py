import json
from apps.api.services.bias_service import analyze_bias

def generate():
    samples = [
        "led aggressive sales team at google",
        "worked as software engineer",
        "supportive marketing assistant from harvard",
        "10 years experience in leadership roles"
    ]

    with open("datasets/processed/bias_dataset.jsonl", "w") as f:
        for text in samples:
            result = analyze_bias(text)

            label = 1 if result["bias_score"] > 0.5 else 0

            f.write(json.dumps({
                "text": text,
                "label": label
            }) + "\n")

generate()