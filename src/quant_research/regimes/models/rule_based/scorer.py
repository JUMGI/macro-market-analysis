import numpy as np
import pandas as pd


class RegimeScorer:

    def score(self, rule_scores_by_regime: dict, model_config: dict) -> pd.DataFrame:
        temperature = model_config.get("temperature", 1.0)

        regime_scores = {}

        for regime, scores in rule_scores_by_regime.items():
            if not scores:
                raise ValueError(f"No rules for regime {regime}")

            df = pd.concat(scores, axis=1)
            regime_scores[regime] = df.mean(axis=1)

        score_df = pd.DataFrame(regime_scores)

        probs = self._softmax(score_df, temperature)

        return probs

    def _softmax(self, scores: pd.DataFrame, temperature: float) -> pd.DataFrame:
        scaled = scores / temperature

        # 🔥 clave: usar pandas correctamente
        max_per_row = scaled.max(axis=1)

        exp = (scaled.sub(max_per_row, axis=0)).apply(np.exp)

        probs = exp.div(exp.sum(axis=1), axis=0)

        return probs