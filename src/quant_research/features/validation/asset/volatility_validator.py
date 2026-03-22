import pandas as pd

from quant_research.features.asset.volatility.compute import compute_features
from quant_research.features.validation.core_validator import validate_features
from quant_research.features.asset.volatility.config import VALIDATION_TOLERANCE


def validate_asset_features(
    asset: str,
    df_raw: pd.DataFrame,
    asset_file,
    verbose: bool = True,
) -> dict:
    """
    Validate volatility features for a single asset.
    """

    if verbose:
        print(f"\n=== VALIDATING VOLATILITY: {asset} ===")

    df_stored = pd.read_parquet(asset_file)
    df_expected = compute_features(df_raw)

    result = validate_features(
        df_expected=df_expected,
        df_stored=df_stored,
        tolerance=VALIDATION_TOLERANCE,
        verbose=verbose,
    )

    result["asset"] = asset

    return result


def validate_universe_features(
    asset_dfs: dict,
    feature_path,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Validate volatility features across all assets.
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