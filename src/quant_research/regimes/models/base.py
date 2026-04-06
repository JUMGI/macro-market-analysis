class BaseRegimeModel:

    def fit(self, X):
        return self

    def predict(self, X):
        raise NotImplementedError("predict() must be implemented")