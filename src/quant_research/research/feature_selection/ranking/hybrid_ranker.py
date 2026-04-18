# feature_selection/ranking/hybrid_ranker.py

from typing import Dict, List, Tuple


class HybridRanker:

    def __init__(self, config: dict):
        self.weights = config.get("weights", {})
        self.top_k = config.get("top_k", 10)

    def rank(self, metrics, groups):

        ranked_groups = {}

        for group_name, features in groups.items():

            scores = []

            for f in features:
                m = metrics.get(f, {})

                score = 0
                for metric, w in self.weights.items():
                    score += w * m.get(metric, 0)

                scores.append((f, score))

            scores.sort(key=lambda x: x[1], reverse=True)

            ranked_groups[group_name] = scores

        # 🔥 NEW STRUCTURE
        return {
            "ranked_groups": ranked_groups,
            "ranker": "hybrid",
            "params": {
                "weights": self.weights,
                "top_k": self.top_k
            }
        }