import pandas as pd
from quant_research.regimes.models.base import BaseRegimeModel


class RuleBasedModel(BaseRegimeModel):

    def __init__(self, config, condition_evaluator, rule_evaluator, scorer):
        super().__init__(config)

        self.condition_evaluator = condition_evaluator
        self.rule_evaluator = rule_evaluator
        self.scorer = scorer

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:

        regimes_cfg = self.config["model"]["regimes"]

        rule_scores_by_regime = {}

        for regime in regimes_cfg:
            regime_name = regime["name"]
            rules = regime.get("rules", [])

            regime_rule_scores = []

            for rule in rules:
                conditions = rule.get("conditions", [])

                condition_scores = [
                    self.condition_evaluator.evaluate(X, cond)
                    for cond in conditions
                ]

                rule_score = self.rule_evaluator.evaluate(condition_scores, rule)
                regime_rule_scores.append(rule_score)

            rule_scores_by_regime[regime_name] = regime_rule_scores

        probs = self.scorer.score(rule_scores_by_regime, self.config["model"])

        return probs