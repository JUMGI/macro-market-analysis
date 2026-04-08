import numpy as np


def compute_confidence(probs):
    return probs.max(axis=1)


def compute_entropy(probs):
    return -(probs * np.log(probs + 1e-12)).sum(axis=1)