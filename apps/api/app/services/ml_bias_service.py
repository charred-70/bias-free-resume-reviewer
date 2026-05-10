import joblib
import numpy as np

from packages.ml_core.features.embeddings import embed

MODEL_PATH = "models/production/bias_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_bias(text: str):

    vector = embed(text)

    vector = np.array([vector])

    probability = model.predict_probability(vector)[0]

    return {
        "bias_probability": float(probability)
    }