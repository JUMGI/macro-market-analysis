# research/core/search_space/builder.py

from typing import Dict, List, Tuple

from .schema import SearchSpace


class SearchSpaceBuilder:

    def __init__(self, config: dict):
        self.config = config

    def build(
        self,
        ranked_groups: Dict[str, List[Tuple[str, float]]],
        required_groups: List[str]
    ) -> SearchSpace:

        feature_space = {}

        feature_cfg = self.config.get("features", {})

        for group in required_groups:

            if group not in ranked_groups:
                raise ValueError(f"Group {group} not found in ranked_groups")

            group_rank = ranked_groups[group]

            cfg = feature_cfg.get(group, {"type": "top_k", "k": 1})

            if cfg["type"] == "top_k":
                k = cfg.get("k", 1)
                candidates = [f for f, _ in group_rank[:k]]

            elif cfg["type"] == "all":
                candidates = [f for f, _ in group_rank]

            else:
                raise ValueError(f"Unknown selection type: {cfg['type']}")

            feature_space[group] = {
                "candidates": candidates,
                "selection": cfg
            }

        param_space = self.config.get("params", {})

        return {
            "features": feature_space,
            "params": param_space
        }