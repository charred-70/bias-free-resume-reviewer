from packages.nlp.sentence_splitter import split_sentences

def score_segments(text: str, ml_model):

    sentences = split_sentences(text)

    results = []

    for s in sentences:

        # placeholder ML scoring per sentence
        score = ml_model.predict(s) if ml_model else 0.2

        results.append({
            "segment": s,
            "risk": round(score, 2)
        })

    return results