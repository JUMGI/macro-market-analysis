import itertools
from typing import Dict, List, Tuple

from quant_research.research.domains.regime.search_spaces.utils import (
    extract_groups_from_regime
)


class RegimeFeatureSampler:

    def __init__(self, top_k: int = 3, max_samples: int = 20):
        self.top_k = top_k
        self.max_samples = max_samples

    def sample(
        self,
        regime_config: dict,
        ranked_groups: Dict[str, List[Tuple[str, float]]]
    ) -> List[Dict[str, str]]:

        required_groups = extract_groups_from_regime(regime_config)

        # 🔹 validar existencia
        for g in required_groups:
            if g not in ranked_groups:
                raise ValueError(f"Group {g} not found in ranked_groups")

        # 🔹 tomar top_k por grupo
        group_candidates = {}

        for g in required_groups:
            candidates = ranked_groups[g][: self.top_k]
            group_candidates[g] = [f for f, _ in candidates]

        # 🔹 generar combinaciones
        group_names = list(group_candidates.keys())
        combinations = list(itertools.product(
            *[group_candidates[g] for g in group_names]
        ))

        # 🔹 limitar
        combinations = combinations[: self.max_samples]

        # 🔹 convertir a dict
        samples = []

        for combo in combinations:
            sample = dict(zip(group_names, combo))
            samples.append(sample)

        return samples