# feature_selection/ranking/normalizers.py

from typing import Dict, List


class BaseNormalizer:
    def fit_transform(self, values: List[float]) -> List[float]:
        raise NotImplementedError


# -------------------------
# Min-Max
# -------------------------
class MinMaxNormalizer(BaseNormalizer):

    def fit_transform(self, values: List[float]) -> List[float]:

        if not values:
            return values

        v_min = min(values)
        v_max = max(values)

        if v_max == v_min:
            return [0.5 for _ in values]  # neutral

        return [(v - v_min) / (v_max - v_min) for v in values]


# -------------------------
# Z-Score
# -------------------------
class ZScoreNormalizer(BaseNormalizer):

    def fit_transform(self, values: List[float]) -> List[float]:

        if not values:
            return values

        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        std = var ** 0.5

        if std == 0:
            return [0.0 for _ in values]

        return [(v - mean) / std for v in values]
    
class RankNormalizer(BaseNormalizer):

    def fit_transform(self, values: List[float]) -> List[float]:

        if not values:
            return values

        # ordenar índices por valor
        sorted_idx = sorted(range(len(values)), key=lambda i: values[i])

        ranks = [0] * len(values)

        # asignar rank
        for rank, idx in enumerate(sorted_idx):
            ranks[idx] = rank

        n = len(values)

        if n == 1:
            return [1.0]

        # convertir a percentiles [0,1]
        return [r / (n - 1) for r in ranks]


# -------------------------
# Factory
# -------------------------
def build_normalizer(name: str):

    if name == "minmax":
        return MinMaxNormalizer()

    if name == "zscore":
        return ZScoreNormalizer()

    if name == "rank":
        return RankNormalizer()

    raise ValueError(f"Unknown normalizer: {name}")