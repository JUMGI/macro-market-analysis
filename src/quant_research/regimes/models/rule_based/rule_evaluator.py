import pandas as pd


class RuleEvaluator:

    def evaluate(self, condition_scores: list[pd.Series], rule_config: dict) -> pd.Series:
        if not condition_scores:
            raise ValueError("No condition scores provided")

        aggregation = rule_config.get("aggregation", "mean")
        weight = rule_config.get("weight", 1.0)

        df = pd.concat(condition_scores, axis=1)

        if aggregation == "mean":
            score = df.mean(axis=1)

        elif aggregation == "min":
            score = df.min(axis=1)

        elif aggregation == "max":
            score = df.max(axis=1)

        else:
            raise ValueError(f"Unknown aggregation: {aggregation}")

        return score * weight