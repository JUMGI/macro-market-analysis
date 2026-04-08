import numpy as np
import pandas as pd


class ConditionEvaluator:

    def evaluate(self, X: pd.DataFrame, condition: dict) -> pd.Series:
        feature = condition["feature"]
        op = condition["op"]
        value = condition["value"]

        scale = condition.get("scale", 1.0)
        transform = condition.get("transform", "linear")

        x = X[feature]

        if op == ">":
            raw = x - value

        elif op == "<":
            raw = value - x

        elif op == "between":
            low, high = value
            center = (low + high) / 2
            raw = -(abs(x - center))

        elif op == "abs>":
            raw = abs(x) - value

        else:
            raise ValueError(f"Unsupported op: {op}")

        score = self._transform(raw, scale, transform)

        return score.clip(0.0, 1.0)

    def _transform(self, raw, scale, transform):
        if transform == "linear":
            return raw / scale

        elif transform == "sigmoid":
            k = 1.0 / scale
            return 1 / (1 + np.exp(-k * raw))

        else:
            raise ValueError(f"Unknown transform: {transform}")