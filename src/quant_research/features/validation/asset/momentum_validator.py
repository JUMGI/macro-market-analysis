# src/quant_research/features/validation/asset/momentum_validator.py

import pandas as pd
from pathlib import Path
from typing import Dict

from quant_research.features.asset.momentum.compute import compute_features
from quant_research.features.validation.core_validator import validate_features
from quant_research.features.asset.momentum.config import VALIDATION_TOLERANCE


# ============================================================
# SINGLE ASSET VALIDATION
# ============================================================

def validate_asset_features(
    asset: str,
    df_raw: pd.DataFrame,
    asset_file: Path,
    verbose: bool = True,
) -> dict:
    """
    Validate momentum features for a single asset.

    Parameters
    ----------
    asset : str
        Asset symbol
    df_raw : pd.DataFrame
        Raw input data (must contain 'adj_close')
    asset_file : Path
        Path to stored feature parquet file
    verbose : bool
        Print validation details

    Returns
    -------
    dict
        {
            "asset": str,
            "status": "PASS" | "WARNING",
            "n_issues": int,
            "failed_features": list[str]
        }
    """

    if verbose:
        print(f"\n=== VALIDATING MOMENTUM: {asset} ===")

    # --------------------------------------------------------
    # Load stored features
    # --------------------------------------------------------
    df_stored = pd.read_parquet(asset_file)

    # --------------------------------------------------------
    # Compute expected features (source of truth)
    # --------------------------------------------------------
    df_expected = compute_features(df_raw)

    # --------------------------------------------------------
    # Run validation engine
    # --------------------------------------------------------
    result = validate_features(
        df_expected=df_expected,
        df_stored=df_stored,
        tolerance=VALIDATION_TOLERANCE,
        verbose=verbose,
    )

    # Attach asset info
    result["asset"] = asset

    return result


# ============================================================
# MULTI-ASSET VALIDATION
# ============================================================

def validate_universe_features(
    asset_dfs: Dict[str, pd.DataFrame],
    feature_path: Path,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Validate momentum features across multiple assets.

    Parameters
    ----------
    asset_dfs : dict[str, pd.DataFrame]
        Mapping: asset -> raw dataframe
    feature_path : Path
        Directory containing feature parquet files
    verbose : bool
        Print per-asset logs

    Returns
    -------
    pd.DataFrame
        Summary table:
        - asset
        - status
        - n_issues
        - failed_features
    """

    results = []

    for asset, df_raw in asset_dfs.items():

        asset_file = feature_path / f"{asset}.parquet"

        result = validate_asset_features(
            asset=asset,
            df_raw=df_raw,
            asset_file=asset_file,
            verbose=verbose,
        )

        results.append(result)

    return pd.DataFrame(results)