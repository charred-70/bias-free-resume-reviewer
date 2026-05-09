from packages.nlp.preprocess import clean_text
from apps.api.app.services.bias_service import analyze_bias

def process_resume(resume_text: str):
    cleaned = clean_text(resume_text)

    bias_result = analyze_bias(cleaned)

    return {
        "cleaned_text": cleaned,
        **bias_result
    }