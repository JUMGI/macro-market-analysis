# ensemble.py
from .base import BaseProcessor

class EnsembleSmoother(BaseProcessor):

    def __init__(self, weight: float = 0.5):
        self.weight = weight
        self.prev = None

    def apply(self, probs):

        if self.prev is None:
            self.prev = probs.copy()
            return probs

        blended = self.weight * probs + (1 - self.weight) * self.prev

        self.prev = blended.copy()

        return blended