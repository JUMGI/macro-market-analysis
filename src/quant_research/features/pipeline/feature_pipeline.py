from pathlib import Path
from typing import List, Optional

import pandas as pd

from quant_research.config.paths import PROCESSED_DATA_PATH, FEATURES_PATH, ASSET_FEATURE_PATH
from quant_research.features.registry.asset_feature_registry import create_registry
from quant_research.data.processed.loaders.asset_processed_loader import (
    AssetProcessedDataLoader
)
from quant_research.features.registry.export_registry import (
    export_feature_registry_snapshot
)



class FeaturePipeline:
    """
    Orchestrates feature computation, validation, and storage.

    Pipeline:
    processed data → compute → (optional asset validation) → save parquet

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
        
       
        # 🔥 Official data interface
        self.loader = AssetProcessedDataLoader(self.processed_path)

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

            df_processed = self.loader.load_asset(asset, start, end)

            for family in families:
                self._process_family(
                    asset=asset,
                    family=family,
                    df_processed=df_processed,
                    validate=validate,
                    overwrite=overwrite,
                    verbose=verbose,
                )
        export_feature_registry_snapshot(
            registry=self.registry,
            output_path=self.features_path /"asset"/ "registry_snapshot.json"
        )
    # ============================================================
    # FAMILY PROCESSING
    # ============================================================

    def _process_family(
        self,
        asset: str,
        family: str,
        df_processed: pd.DataFrame,
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

        df_features = spec.compute_fn(df_processed)

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
        # Optional asset-level validation
        # --------------------------------------------
        if validate:
            self._run_asset_validation(
                asset=asset,
                family=family,
                df_processed=df_processed,
                output_path=output_path,
            )

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
    # ASSET-LEVEL VALIDATION (INTERNAL)
    # ============================================================

    def _run_asset_validation(
        self,
        asset: str,
        family: str,
        df_processed: pd.DataFrame,
        output_path: Path,
    ):
        """
        Validate features for a single asset (deterministic check).
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
            df_raw=df_processed,  # naming inside validator
            asset_file=output_path,
            verbose=True,
        )

    # ============================================================
    # UNIVERSE VALIDATION (ANALYTICAL)
    # ============================================================

    def run_universe_validation(
        self,
        assets: List[str],
        family: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ):
        """
        Run multi-asset (universe-level) validation.

        This is a diagnostic tool, not part of the core pipeline.
        """

        if family == "momentum":
            from quant_research.features.validation.asset.momentum_validator import (
                validate_universe_features
            )
        elif family == "volatility":
            from quant_research.features.validation.asset.volatility_validator import (
                validate_universe_features
            )
        else:
            raise ValueError(f"No validator available for family: {family}")

        # ----------------------------------------
        # Load processed data
        # ----------------------------------------

        asset_dfs = self.loader.load_universe(assets, start, end)

        # ----------------------------------------
        # Feature path
        # ----------------------------------------

        feature_path = self.features_path / "asset" / family

        # ----------------------------------------
        # Run validation
        # ----------------------------------------

        results = validate_universe_features(
            asset_dfs=asset_dfs,
            feature_path=feature_path,
            verbose=True,
        )

        return results