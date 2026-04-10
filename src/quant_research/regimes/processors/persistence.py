# persistence.py
from .base import BaseProcessor

class PersistenceProcessor(BaseProcessor):

    def __init__(self, min_duration: int):
        self.min_duration = min_duration

    def apply(self, probs):

        labels = probs.idxmax(axis=1)
        labels = labels.copy()

        current = labels.iloc[0]
        count = 1

        for i in range(1, len(labels)):
            if labels.iloc[i] == current:
                count += 1
            else:
                if count < self.min_duration:
                    labels.iloc[i-count:i] = current
                current = labels.iloc[i]
                count = 1

        # reconstruir probs (hard assignment)
        return self._labels_to_probs(labels, probs.columns)

    def _labels_to_probs(self, labels, columns):
        import pandas as pd
        out = pd.DataFrame(0, index=labels.index, columns=columns)

        for col in columns:
            out[col] = (labels == col).astype(float)

        return out