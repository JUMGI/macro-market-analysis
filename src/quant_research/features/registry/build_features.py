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

from pathlib import Path
import pandas as pd
from typing import List
from .feature_spec import FeatureSpec
from quant_research.config.paths import MOMENTUM_FEATURE_PATH, VOLATILITY_FEATURE_PATH

# ============================================================
# Momentum imports
# ============================================================
from quant_research.features.asset.momentum.features_engine import compute_momentum_features
from quant_research.features.asset.momentum.config import (
    LOOKBACK_WINDOWS as MOM_LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW as MOM_NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS as MOM_SMOOTH_WINDOWS,
    MSI_WEIGHTS as MOM_MSI_WEIGHTS,
    MOM_ALIGN_THRESHOLD,
    MSI_SMOOTH_WINDOW as MOM_MSI_SMOOTH_WINDOW,
)

# ============================================================
# Volatility imports
# ============================================================
from quant_research.features.asset.volatility.feature_engine import build_volatility_features
from quant_research.features.asset.volatility.config import (
    LOOKBACK_WINDOWS as VOL_LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW as VOL_NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS as VOL_SMOOTH_WINDOWS,
    VOV_WINDOWS,
    TERM_STRUCTURE_PAIRS,
    VSI_HORIZONS,
    VSI_WEIGHTS,
    VSI_SMOOTH_WINDOW,
)

# ============================================================
# Helpers
# ============================================================

def extract_window(name: str):
    """Extract numeric window from feature name if present"""
    for token in name.split("_"):
        if token.isdigit():
            return int(token)
    return None

# family → input column mapping
FAMILY_INPUTS = {
    "volatility": "log_ret",
    "momentum": "adj_close",
    "liquidity": "volume",  # próxima familia
}

def build_features_from_path(base_path: Path, family: str, compute_fn) -> List[FeatureSpec]:
    """
    Build FeatureSpec objects dynamically reading any parquet file from a family folder
    and assign the correct input column according to family.
    """
    if not base_path.exists():
        raise FileNotFoundError(f"Folder not found: {base_path}")

    first_parquet = next(base_path.glob("*.parquet"), None)
    if first_parquet is None:
        raise FileNotFoundError(f"No parquet found in {base_path}")

    df = pd.read_parquet(first_parquet)
    column_names = df.columns.tolist()

    # Assign input column dynamically by family
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
                inputs=[input_column],  # automatic by family
                parameters={"window": extract_window(col)} if extract_window(col) else {},
                compute_fn=compute_fn,
                frequency="daily"
            )
        )
    return specs

# ============================================================
# Momentum compute wrapper
# ============================================================

def compute_momentum_wrapper(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Wrapper for compute_momentum_features to fix the parameters from config
    """
    return compute_momentum_features(
        df_raw=df_raw,
        lookback_windows=MOM_LOOKBACK_WINDOWS,
        normalization_window=MOM_NORMALIZATION_WINDOW,
        smooth_windows=MOM_SMOOTH_WINDOWS,
        msi_weights=MOM_MSI_WEIGHTS,
        mom_align_threshold=MOM_ALIGN_THRESHOLD,
        msi_smooth_window=MOM_MSI_SMOOTH_WINDOW,
    )

# ============================================================
# Builders
# ============================================================

def build_momentum_features_spec() -> List[FeatureSpec]:
    """Build all momentum FeatureSpec objects"""
    return build_features_from_path(
        Path(MOMENTUM_FEATURE_PATH),
        family="momentum",
        compute_fn=compute_momentum_wrapper
    )

def build_volatility_features_spec() -> List[FeatureSpec]:
    """Build all volatility FeatureSpec objects"""
    return build_features_from_path(
        Path(VOLATILITY_FEATURE_PATH),
        family="volatility",
        compute_fn=build_volatility_features
    )