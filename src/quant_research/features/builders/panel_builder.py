"""
Feature Panel Builder
---------------------

Builds a cross-asset feature panel from per-asset feature files.

The storage layer keeps features saved per asset (Parquet files).
This module reconstructs a research-ready panel with a MultiIndex
column structure.

Output structure:

    index   → date
    columns → MultiIndex (feature, asset)

Example:

    feature        MOM_21           MOM_63
    asset             BTC    SPY       BTC    SPY
    date
    2020-01-01
    2020-01-02
"""

import pandas as pd

from quant_research.features.loaders import asset_feature_loader


# ============================================================
# Feature Panel Builder
# ============================================================

def build_feature_panel(
    assets,
    families,
):
    """
    Build a cross-asset feature panel.

    Parameters
    ----------
    assets : list[str]

        List of assets to load.

        Example:
            ["BTC", "SPY", "QQQ"]


    families : list[str]

        Feature families defined in the registry.

        Example:
            ["momentum", "volatility"]


    Returns
    -------
    pandas.DataFrame

        Cross-asset feature panel with structure:

            index   → date
            columns → MultiIndex (feature, asset)

        Shape:

            (n_dates, n_features × n_assets)
    """

    # ========================================================
    # Load features for all assets
    # ========================================================

    asset_dict = asset_feature_loader.load_asset_features(
        assets=assets,
        families=families
    )

    dfs = []

    # ========================================================
    # Rebuild MultiIndex columns
    # ========================================================

    for asset, df in asset_dict.items():

        # Convert feature columns → MultiIndex(feature, asset)
        df.columns = pd.MultiIndex.from_product(
            [df.columns, [asset]],
            names=["feature", "asset"]
        )

        dfs.append(df)

    # ========================================================
    # Combine all assets into one panel
    # ========================================================

    panel = pd.concat(dfs, axis=1)

    # Sort columns for deterministic ordering
    panel = panel.sort_index(axis=1)

    return panel