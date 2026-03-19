# ============================================================
# Momentum Feature Validator
# ============================================================

import pandas as pd
import numpy as np

from quant_research.features.asset.momentum.features_engine import build_momentum_features
from .config import (
    LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS,
    MSI_WEIGHTS,
    MOM_ALIGN_THRESHOLD,
    MSI_SMOOTH_WINDOW,
    VALIDATION_TOLERANCE,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def max_diff(a: pd.Series, b: pd.Series) -> float:
    return (a - b).abs().max()


def check_diff(name: str, diff: float, tol: float, verbose: bool) -> bool:
    if pd.isna(diff):
        if verbose:
            print(f"{name}: SKIP")
        return True

    if diff < tol:
        if verbose:
            print(f"{name}: OK")
        return True
    else:
        if verbose:
            print(f"{name}: WARNING ⚠️ (diff={diff:.2e})")
        return False


# ------------------------------------------------------------
# Core validator
# ------------------------------------------------------------
def validate_asset_features(
    asset: str,
    df_raw: pd.DataFrame,
    asset_file,
    verbose: bool = True,
) -> dict:
    """
    Validate momentum features for a single asset.

    Returns:
        dict with:
        - asset
        - status (PASS / WARNING)
        - n_issues
        - failed_features (list)
    """

    df_stored = pd.read_parquet(asset_file)

    if verbose:
        print(f"\n=== VALIDATING: {asset} ===")

    # --------------------------------------------------------
    # Compute expected features (SOURCE OF TRUTH)
    # --------------------------------------------------------
    df_expected = build_momentum_features(df_raw)

    # --------------------------------------------------------
    # Align columns
    # --------------------------------------------------------
    common_cols = sorted(set(df_stored.columns) & set(df_expected.columns))

    all_ok = True
    failed_features = []

    # --------------------------------------------------------
    # Compare values
    # --------------------------------------------------------
    for col in common_cols:
        diff = max_diff(df_stored[col], df_expected[col])

        ok = check_diff(col, diff, VALIDATION_TOLERANCE, verbose)

        if not ok:
            failed_features.append(col)

        all_ok = all_ok and ok

    # --------------------------------------------------------
    # Extra columns check
    # --------------------------------------------------------
    extra_cols = set(df_stored.columns) - set(df_expected.columns)

    if extra_cols:
        all_ok = False
        failed_features.extend(sorted(extra_cols))

        if verbose:
            print("\nUnexpected columns in stored features:")
            for col in sorted(extra_cols):
                print(f" - {col}")

    # --------------------------------------------------------
    # Missing columns check
    # --------------------------------------------------------
    missing_cols = set(df_expected.columns) - set(df_stored.columns)

    if missing_cols:
        all_ok = False
        failed_features.extend(sorted(missing_cols))

        if verbose:
            print("\nMissing columns in stored features:")
            for col in sorted(missing_cols):
                print(f" - {col}")

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------
    status = "PASS" if all_ok else "WARNING"

    if verbose:
        print(f"\n=== RESULT: {status} ===")

    return {
        "asset": asset,
        "status": status,
        "n_issues": len(failed_features),
        "failed_features": failed_features,
    }


# ------------------------------------------------------------
# Multi-asset summary
# ------------------------------------------------------------
def validate_universe_features(
    asset_dfs: dict,
    feature_path,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Validate all assets and return summary table.
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

        results.append({
            "asset": result["asset"],
            "status": result["status"],
            "n_issues": result["n_issues"],
            "failed_features": result["failed_features"],
        })

    return pd.DataFrame(results)