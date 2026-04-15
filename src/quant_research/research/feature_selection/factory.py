from quant_research.research.feature_selection.policies.hybrid_policy import HybridPolicy


def build_feature_selector(config):

    method = config.get("method", "hybrid")

    if method == "hybrid":
        return HybridPolicy()

    raise ValueError(f"Unknown feature selection method: {method}")