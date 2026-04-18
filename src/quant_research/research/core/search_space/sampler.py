# research/core/search_space/sampler.py

import itertools
from typing import List

from .schema import SearchSpace, Sample


class SearchSpaceSampler:

    def __init__(self, max_samples: int = 20):
        self.max_samples = max_samples

    def sample(self, space: SearchSpace) -> List[Sample]:

        # 🔹 feature combinations
        feature_groups = list(space["features"].keys())

        feature_candidates = [
            space["features"][g]["candidates"]
            for g in feature_groups
        ]

        feature_combos = list(itertools.product(*feature_candidates))

        # 🔹 param combinations
        param_names = list(space["params"].keys())

        param_candidates = [
            space["params"][p]["values"]
            for p in param_names
        ] if param_names else [[]]

        param_combos = list(itertools.product(*param_candidates))

        # 🔹 joint combinations
        samples = []

        for f_combo in feature_combos:
            for p_combo in param_combos:

                sample = {
                    "features": dict(zip(feature_groups, f_combo)),
                    "params": dict(zip(param_names, p_combo))
                }

                samples.append(sample)

                if len(samples) >= self.max_samples:
                    return samples

        return samples