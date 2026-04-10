# hysteresis.py
from .base import BaseProcessor

class HysteresisProcessor(BaseProcessor):

    def __init__(self, enter_threshold: float, exit_threshold: float):
        self.enter = enter_threshold
        self.exit = exit_threshold

    def apply(self, probs):

        labels = []
        current = None

        for i, row in probs.iterrows():

            if current is None:
                current = row.idxmax()

            prob_current = row[current]

            if prob_current < self.exit:
                # evaluar entrada
                best = row.idxmax()
                if row[best] > self.enter:
                    current = best

            labels.append(current)

        return self._labels_to_probs(labels, probs.columns, probs.index)

    def _labels_to_probs(self, labels, columns, index):
        import pandas as pd

        out = pd.DataFrame(0, index=index, columns=columns)

        for col in columns:
            out[col] = [1.0 if l == col else 0.0 for l in labels]

        return out