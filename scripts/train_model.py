import numpy as np
import json
import joblib
from packages.ml_core.features.embeddings import embed
from packages.ml_core.models.model import BiasModel

DATASET_PATH = "datasets/processed/bias.dataset.jsonl"
MODEL_OUTPUT = "models/production/bias_model.pkl"

def load():
    X, y = [], []

    with open(DATASET_PATH, "r") as f:
        for line in f:
            item = json.loads(line)
            vector = embed(item["text"])
            X.append(vector)
            y.append(item["label"])

    return np.array(X), np.array(y)

def train():
    print("Loading dataset...")

    X, y = load()

    print("Training model...")

    model = BiasModel()
    model.train(X, y)

    print("Saving model...")

    joblib.dump(model, MODEL_OUTPUT)

    print("Training complete.")

if __name__ == "__main__":
    train()
