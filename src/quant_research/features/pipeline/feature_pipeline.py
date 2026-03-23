from pathlib import Path
from typing import List, Optional, Dict

import pandas as pd

from quant_research.config.paths import PROCESSED_DATA_PATH, FEATURES_PATH
from quant_research.features.registry.asset_feature_registry import create_registry


class FeaturePipeline:
    """
    Orchestrates feature computation, validation, and storage.

    Pipeline:
    raw data → compute → (optional validate) → save parquet

    Output structure:
    data/features/asset/{family}/{asset}.parquet
    """

    # ============================================================
    # INIT
    # ============================================================

    def __init__(
        self,
        processed_path: Path = PROCESSED_DATA_PATH,
        features_path: Path = FEATURES_PATH,
    ):
        self.processed_path = Path(processed_path)
        self.features_path = Path(features_path)

        self.registry = create_registry()

    # ============================================================
    # PUBLIC API
    # ============================================================

    def run(
        self,
        assets: List[str],
        families: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        validate: bool = False,
        overwrite: bool = True,
        verbose: bool = True,
    ):
        """
        Run feature pipeline for multiple assets and families.
        """

        for asset in assets:
            if verbose:
                print(f"\n=== PROCESSING ASSET: {asset} ===")

            df_raw = self._load_raw(asset, start, end)

            for family in families:
                self._process_family(
                    asset=asset,
                    family=family,
                    df_raw=df_raw,
                    validate=validate,
                    overwrite=overwrite,
                    verbose=verbose,
                )

    # ============================================================
    # RAW DATA
    # ============================================================

    def _load_raw(
        self,
        asset: str,
        start: Optional[str],
        end: Optional[str],
    ) -> pd.DataFrame:

        path = self.processed_path / f"{asset}.parquet"

        if not path.exists():
            raise FileNotFoundError(f"Raw data not found: {path}")

        df = pd.read_parquet(path)

        if start:
            df = df[df.index >= pd.to_datetime(start)]

        if end:
            df = df[df.index <= pd.to_datetime(end)]

        return df

    # ============================================================
    # FAMILY PROCESSING
    # ============================================================

    def _process_family(
        self,
        asset: str,
        family: str,
        df_raw: pd.DataFrame,
        validate: bool,
        overwrite: bool,
        verbose: bool,
    ):
        spec = self._get_family_spec(family)

        output_path = self._get_output_path(asset, family)

        if output_path.exists() and not overwrite:
            if verbose:
                print(f"Skipping {family} ({asset}) — already exists")
            return

        if verbose:
            print(f"Computing {family} features...")

        df_features = spec.compute_fn(df_raw)

        # --------------------------------------------
        # Schema validation (critical)
        # --------------------------------------------
        self._validate_schema(spec, df_features)

        # --------------------------------------------
        # Save
        # --------------------------------------------
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_features.to_parquet(output_path)

        if verbose:
            print(f"Saved → {output_path}")

        # --------------------------------------------
        # Optional value validation
        # --------------------------------------------
        if validate:
            self._run_validation(asset, family, df_raw, output_path)

    # ============================================================
    # SPEC RESOLUTION
    # ============================================================

    def _get_family_spec(self, family: str):
        """
        Retrieve the FeatureSpec representing the family.
        """

        specs = self.registry.get_by_family(family)

        if not specs:
            raise ValueError(f"No features found for family: {family}")

        # all specs share same compute_fn → take first
        return specs[0]

    # ============================================================
    # PATHS
    # ============================================================

    def _get_output_path(self, asset: str, family: str) -> Path:
        return self.features_path / "asset" / family / f"{asset}.parquet"

    # ============================================================
    # SCHEMA VALIDATION
    # ============================================================

    def _validate_schema(self, spec, df_features: pd.DataFrame):
        expected = set(spec.output_columns)
        actual = set(df_features.columns)

        if expected != actual:
            missing = expected - actual
            extra = actual - expected

            raise ValueError(
                f"Schema mismatch for {spec.name}\n"
                f"Missing: {missing}\n"
                f"Extra: {extra}"
            )

    # ============================================================
    # VALUE VALIDATION (optional)
    # ============================================================

    def _run_validation(
        self,
        asset: str,
        family: str,
        df_raw: pd.DataFrame,
        output_path: Path,
    ):
        """
        Hook to asset-specific validators.
        """

        if family == "momentum":
            from quant_research.features.validation.asset.momentum_validator import (
                validate_asset_features
            )

        elif family == "volatility":
            from quant_research.features.validation.asset.volatility_validator import (
                validate_asset_features
            )

        else:
            return

        validate_asset_features(
            asset=asset,
            df_raw=df_raw,
            asset_file=output_path,
            verbose=True,
        )