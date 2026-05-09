from packages.nlp.preprocess import clean_text

def process_resume(resume_text: str):
    cleaned = clean_text(resume_text)

    return {
        "cleaned_text": cleaned,
        "length": len(cleaned)
    }