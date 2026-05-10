from packages.nlp.preprocess import clean_text
from packages.nlp.parser import extract_text_from_pdf
from apps.api.app.services.bias_service import analyze_bias
from packages.bias_detector.rewrite_engine import rewrite_resume
from packages.nlp.section_parser import segment_resume

def process_resume(resume_text: str):

    cleaned = clean_text(resume_text)

    bias_result = analyze_bias(cleaned)

    rewrite_result = rewrite_resume(cleaned)

    return {
        "cleaned_text": cleaned,
        **bias_result,
        "rewrites": rewrite_result
    }

def process_pdf(file_path: str):

    raw_text = extract_text_from_pdf(file_path)

    cleaned = clean_text(raw_text)

    sections = segment_resume(cleaned)

    bias_result = analyze_bias(cleaned)

    rewrite_result = rewrite_resume(cleaned)

    return {
        "cleaned_text": cleaned,
        "section": sections,
        **bias_result,
        "rewrites": rewrite_result
    }