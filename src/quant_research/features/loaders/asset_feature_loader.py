"""
Asset Feature Loader
--------------------

Load asset-level features stored as parquet files.

Responsibilities

- load features for one asset
- load features for multiple assets
- filter using the feature registry
- combine feature families
"""

from pathlib import Path
import pandas as pd

from quant_research.features.utils.registry_helpers import get_features


# ============================================================
# Paths
# ============================================================

from quant_research.config.paths import FEATURES_PATH
from quant_research.config.paths import ASSET_FEATURE_PATH


# ============================================================
# Load Single Family
# ============================================================

def load_asset_family(asset: str, family: str) -> pd.DataFrame:
    """
    Load one feature family for a given asset.
    """

    file_path = ASSET_FEATURE_PATH / family / f"{asset}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Feature file not found: {file_path}")

    df = pd.read_parquet(file_path)

    return df



# ============================================================
# Load One or Multiple Assets
# ============================================================

def load_asset_features(
    assets,
    families=None,
    registry_filter=True
):
    """
    Load features for one or multiple assets.
    """

    if isinstance(assets, str):
        assets = [assets]

    if families is None:
        families = ["Momentum", "Volatility"]

    asset_data = {}

    for asset in assets:

        dfs = []

        for family in families:

            df = load_asset_family(asset, family)

            if registry_filter:

                allowed = get_features(family)

                df = df[[c for c in df.columns if c in allowed]]

            dfs.append(df)

        df_all = pd.concat(dfs, axis=1)
        df_all = df_all.sort_index()

        asset_data[asset] = df_all

    return asset_data
