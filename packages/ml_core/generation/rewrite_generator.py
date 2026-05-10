from transformers import pipeline

# lightweight model for hackathon MVP
generator = pipeline("text-generation", model="google/flan-t5-base")


def rewrite_with_transformer(text: str):

    prompt = f"""
    Rewrite this resume to remove bias while preserving meaning:

    {text}

    Make it neutral, professional, and non-discriminatory.
    """

    result = generator(prompt, max_length=256, do_sample=False)

    return result[0]["generated_text"]