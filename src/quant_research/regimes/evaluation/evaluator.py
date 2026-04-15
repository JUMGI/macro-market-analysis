from quant_research.regimes.evaluation.metrics.structure import (
    compute_persistence,
    compute_transition_rate,
    compute_entropy_mean,
)

from quant_research.regimes.evaluation.metrics.separation import (
    compute_prob_spread,
)

from quant_research.regimes.evaluation.metrics.economic import (
    compute_conditional_stats,
    compute_forward_returns,
    compute_predictive_correlation,
    compute_drawdown_capture,
)
from quant_research.regimes.evaluation.metrics.economic import (
    compute_hit_ratio,
    compute_transition_pnl,
    compute_regime_drawdown,
)

from quant_research.research.domains.regime.objective import compute_grouped_score


class RegimeEvaluator:

    def __init__(self, config: dict):
        self.config = config
        

    def evaluate(self, regime_df, returns=None):

        metrics = {}

        # --- structure ---
        metrics["persistence"] = compute_persistence(regime_df)
        metrics["transition_rate"] = compute_transition_rate(regime_df)
        metrics["entropy_mean"] = compute_entropy_mean(regime_df)

        # --- separation ---
        metrics["prob_spread"] = compute_prob_spread(regime_df)

        # --- economic ---
        if returns is not None:
            metrics.update(compute_conditional_stats(regime_df, returns))
            metrics.update(compute_forward_returns(regime_df, returns))
            metrics.update(compute_predictive_correlation(regime_df, returns))
            metrics.update(compute_drawdown_capture(regime_df, returns))

            # nuevas
            metrics.update(compute_hit_ratio(regime_df, returns))
            metrics.update(compute_transition_pnl(regime_df, returns))
            metrics.update(compute_regime_drawdown(regime_df, returns))
        
        self._validate_metrics(metrics)     
        # --- grouped score ---
        scores = compute_grouped_score(metrics, self.config)

        return {
            "metrics": metrics,
            "scores": scores
        }
    def _validate_metrics(self, metrics):

        required = (
            list(self.config["structure"].keys()) +
            list(self.config["economic"].keys()) +
            list(self.config["decision"].keys())
        )

        missing = [k for k in required if k not in metrics]

        if missing:
            if self.config.get("strict", False):
                raise ValueError(f"Missing metrics: {missing}")
            else:
                print(f"[WARN] Missing metrics: {missing}")