# src/quant_research/features/registry/build_features.py

"""
build_features.py

Dynamically constructs FeatureSpec objects for all asset-level features 
(momentum and volatility) by reading parquet files and linking each feature 
to its corresponding compute function.

- Eliminates hardcoding of feature names.
- Uses paths from quant_research.config.paths
- Uses parameters from the respective config.py files
- Returns a list of FeatureSpec objects ready for FeatureRegistry.
"""

# src/quant_research/features/registry/build_features.py

from pathlib import Path
import pandas as pd
from typing import List
from .feature_spec import FeatureSpec
from quant_research.config.paths import MOMENTUM_FEATURE_PATH, VOLATILITY_FEATURE_PATH

# ============================================================
# Momentum engine (NUEVO)
# ============================================================

from quant_research.features.asset.momentum.feature_engine import build_momentum_features

# ============================================================
# Volatility engine
# ============================================================

from quant_research.features.asset.volatility.feature_engine import build_volatility_features

# ============================================================
# Helpers
# ============================================================

def extract_window(name: str):
    for token in name.split("_"):
        if token.isdigit():
            return int(token)
    return None


FAMILY_INPUTS = {
    "volatility": "log_ret",
    "momentum": "adj_close",
    "liquidity": "volume",
}


def build_features_from_path(base_path: Path, family: str, compute_fn) -> List[FeatureSpec]:

    if not base_path.exists():
        raise FileNotFoundError(f"Folder not found: {base_path}")

    first_parquet = next(base_path.glob("*.parquet"), None)
    if first_parquet is None:
        raise FileNotFoundError(f"No parquet found in {base_path}")

    df = pd.read_parquet(first_parquet)
    column_names = df.columns.tolist()

    input_column = FAMILY_INPUTS.get(family)
    if input_column is None:
        raise ValueError(f"No input column defined for family '{family}'")

    specs = []

    for col in column_names:
        specs.append(
            FeatureSpec(
                name=col,
                family=family,
                asset_level="asset",
                column=col,
                inputs=[input_column],
                parameters={},
                compute_fn=compute_fn,  # <- engine directo
                frequency="daily",
            )
        )

    return specs


# ============================================================
# BUILDERS
# ============================================================

def build_momentum_features_spec() -> List[FeatureSpec]:
    return build_features_from_path(
        Path(MOMENTUM_FEATURE_PATH),
        family="momentum",
        compute_fn=build_momentum_features  # <- engine nuevo
    )


def build_volatility_features_spec() -> List[FeatureSpec]:
    return build_features_from_path(
        Path(VOLATILITY_FEATURE_PATH),
        family="volatility",
        compute_fn=build_volatility_features
    )