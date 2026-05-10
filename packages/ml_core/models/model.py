from sklearn.linear_model import LogisticRegression

class BiasModel:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_probability(self, X):
        return self.model.predict_proba(X)[:, 1]