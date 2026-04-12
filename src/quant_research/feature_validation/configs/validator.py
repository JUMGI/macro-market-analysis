import inspect
from quant_research.feature_validation.metrics.registry import METRIC_REGISTRY


def validate_validation_config(config: dict):
    """
    Validates that config is consistent with metric implementations.
    """

    if "metrics" not in config:
        raise ValueError("Config must contain 'metrics'")

    metrics_cfg = config["metrics"]

    for metric_name, metric_cfg in metrics_cfg.items():

        # -------------------------
        # 1. Metric exists
        # -------------------------
        if metric_name not in METRIC_REGISTRY:
            raise ValueError(f"Metric '{metric_name}' not found in registry")

        func = METRIC_REGISTRY[metric_name]

        # -------------------------
        # 2. Params validation
        # -------------------------
        params_cfg = metric_cfg.get("params", {})

        sig = inspect.signature(func)
        valid_params = set(sig.parameters.keys())

        # ignoramos estos params comunes
        valid_params.discard("series")
        valid_params.discard("full_df")

        for param in params_cfg.keys():
            if param not in valid_params:
                raise ValueError(
                    f"Invalid param '{param}' for metric '{metric_name}'"
                )

        # -------------------------
        # 3. Required params (opcional)
        # -------------------------
        for name, p in sig.parameters.items():

            if name in ["series", "full_df"]:
                continue

            if p.default is inspect.Parameter.empty:
                # es obligatorio
                if name not in params_cfg:
                    raise ValueError(
                        f"Missing required param '{name}' for metric '{metric_name}'"
                    )