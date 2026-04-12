from typing import Dict
import pandas as pd

from quant_research.feature_validation.metrics.registry import METRIC_REGISTRY

from quant_research.feature_validation.metrics.stability import compute_stability
from quant_research.feature_validation.metrics.autocorr import compute_autocorr
from quant_research.feature_validation.metrics.missing import compute_missing
from quant_research.feature_validation.metrics.redundancy import compute_redundancy


class SystemicValidationProfile:

    def __init__(self, config: Dict = None):
        self.config = config or {}

        if config is None:
            raise ValueError("SystemicValidationProfile requires a config")

        if "metrics" not in config:
            raise ValueError("Config must include 'metrics'")

        self.metrics_config = config["metrics"]

    def evaluate(self, series, full_df):

        results = {}

        for metric_name, metric_cfg in self.metrics_config.items():

            if not metric_cfg.get("enabled", False):
                continue

            if metric_name not in METRIC_REGISTRY:
                raise ValueError(f"Metric '{metric_name}' not found")

            func = METRIC_REGISTRY[metric_name]
            params = metric_cfg.get("params", {})

            try:
                value = func(series=series, full_df=full_df, **params)
                results[metric_name] = value

            except Exception as e:
                results[metric_name] = {"error": str(e)}

        return results
    

