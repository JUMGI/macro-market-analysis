from typing import List
from .feature_spec import FeatureSpec

# Momentum
from quant_research.features.asset.momentum.compute import (
    compute_features as momentum_compute,
    get_feature_columns as momentum_columns
)

# Volatility
from quant_research.features.asset.volatility.compute import (
    compute_features as volatility_compute,
    get_feature_columns as volatility_columns
)


# ============================================================
# BUILDERS
# ============================================================

def build_momentum_spec() -> FeatureSpec:

    return FeatureSpec(
        name="momentum",
        family="momentum",
        level="asset",
        inputs=["adj_close"],
        parameters={},
        compute_fn=momentum_compute,
        output_columns=momentum_columns(),
        frequency="daily",
    )


def build_volatility_spec() -> FeatureSpec:

    return FeatureSpec(
        name="volatility",
        family="volatility",
        level="asset",
        inputs=["log_ret"],
        parameters={},
        compute_fn=volatility_compute,
        output_columns=volatility_columns(),
        frequency="daily",
    )


def build_all_feature_specs() -> List[FeatureSpec]:
    """
    Entry point for registry.
    """

    return [
        build_momentum_spec(),
        build_volatility_spec(),
    ]