from quant_research.research.feature_selection.ranking.normalizers import build_normalizer


class HybridRanker:

    def __init__(self, config: dict):
        self.weights = config.get("weights", {})
        self.normalizer_name = config.get("normalizer", "minmax")

        if not self.weights:
            raise ValueError("HybridRanker requires weights")

        self.normalizer = build_normalizer(self.normalizer_name)

    def rank(self, metrics, groups):

        ranked_groups = {}

        for group_name, features in groups.items():

            # -------------------------
            # 1. collect raw metric values
            # -------------------------
            metric_values = {
                metric: [metrics.get(f, {}).get(metric, 0) for f in features]
                for metric in self.weights.keys()
            }

            # -------------------------
            # 2. normalize per metric
            # -------------------------
            normalized = {}

            for metric, values in metric_values.items():
                normalized[metric] = self.normalizer.fit_transform(values)

            # -------------------------
            # 3. compute scores
            # -------------------------
            scores = []

            for i, f in enumerate(features):

                score = 0

                for metric, w in self.weights.items():
                    score += w * normalized[metric][i]

                scores.append((f, score))

            scores.sort(key=lambda x: x[1], reverse=True)

            ranked_groups[group_name] = scores

        return {
            "ranked_groups": ranked_groups,
            "ranker": "hybrid",
            "params": {
                "weights": self.weights,
                "normalizer": self.normalizer_name
            }
        }