# smoothing.py

from .base import BaseProcessor

class RollingMeanSmoother(BaseProcessor):

    def __init__(self, window: int):
        self.window = window

    def apply(self, probs):
        return probs.rolling(self.window, min_periods=1).mean()
    

# smoothing.py

class ExponentialSmoother(BaseProcessor):

    def __init__(self, alpha: float):
        self.alpha = alpha

    def apply(self, probs):
        return probs.ewm(alpha=self.alpha, adjust=False).mean()