# thresholding.py

from .base import BaseProcessor

class ThresholdingProcessor(BaseProcessor):

    def __init__(self, threshold: float):
        self.threshold = threshold

    def apply(self, probs):

        mask = probs >= self.threshold
        filtered = probs * mask

        # renormalizar
        row_sum = filtered.sum(axis=1)

        # evitar división por 0
        row_sum = row_sum.replace(0, 1)

        return filtered.div(row_sum, axis=0)