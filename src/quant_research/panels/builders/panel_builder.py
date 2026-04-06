from typing import List, Optional, Dict
import pandas as pd
import json

from quant_research.panels.utils.alignment import align_and_concat
from quant_research.panels.utils.validation import validate_assets
from quant_research.panels.contracts import enforce_panel_contract  # NEW


class PanelBuilder:
    """
    Build cross-asset feature panels from per-asset feature datasets.

    This class orchestrates the transformation from asset-level feature
    data (time series per asset) into a unified panel suitable for
    cross-sectional analysis, machine learning, and allocation research.

    The resulting panel follows a standardized structure:
    - index: datetime
    - columns: MultiIndex (feature, asset)
    """

    def __init__(self, feature_loader, processed_loader, processed_metadata_path):
        """
        Initialize the PanelBuilder.

        Parameters
        ----------
        feature_loader : object
            Loader responsible for retrieving feature data.
            Must implement:
                load_asset_features(family: str, asset: str) -> pd.DataFrame
        """
        self.loader = feature_loader
        self.processed_loader = processed_loader
        # ----------------------------------------
        # LOAD METADATA
        # ----------------------------------------
        with open(processed_metadata_path, "r") as f:
            metadata = json.load(f)

        self.processed_feature_map = metadata["feature_map"]   # raw → panel
        self.available_processed_features = set(metadata["features"])
    # ============================================================
    # PUBLIC API
    # ============================================================

    def build_panel(
        self,
        assets: List[str],
        families: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        alignment: str = "union",
        nan_policy: str = "keep",
        structure: str = "multiindex",
        validate: bool = True,
        include_processed: Optional[List[str]] = None,   # 👈 NEW
    ) -> pd.DataFrame:
        """
        Build a cross-asset feature panel.

        Parameters
        ----------
        assets : list[str]
            List of asset identifiers (e.g., ["BTC", "SPY"]).
        families : list[str]
            Feature families to include (e.g., ["momentum", "volatility"]).
        start : str, optional
            Start date filter (inclusive).
        end : str, optional
            End date filter (inclusive).
        alignment : str
            Alignment method across assets:
                - "union": include all timestamps (outer join)
                - "intersection": only common timestamps (inner join)
        nan_policy : str
            Strategy to handle missing values:
                - "keep": leave NaNs unchanged
                - "drop": drop rows with any NaNs
                - "ffill": forward fill
                - "bfill": backward fill
        structure : str
            Output column structure:
                - "multiindex": (asset, feature)
                - "flat": "ASSET_FEATURE"
        validate : bool
            Whether to run structural validation on asset data.
        include_processed: list[str]
            List of columns from processed data: Typical ["log_ret", "adj_close"]

        Returns
        -------
        pd.DataFrame
            Cross-asset panel with datetime index and feature columns.
        """

        # 1. Load asset-level feature data
        asset_data = self._load_data(assets, families, start, end)

        # 2. Merge feature families per asset
        # ------------------------------------------------------------
        # NEW: Load and merge processed data
        # ------------------------------------------------------------
        # 2. Merge feature families per asset
        merged_assets = self._merge_families(asset_data)
        
        # ------------------------------------------------------------
        # DEFAULT: include all processed features
        # ------------------------------------------------------------

        if include_processed is None:
            include_processed = sorted(self.available_processed_features)

        # ------------------------------------------------------------
        # LOAD PROCESSED
        # ------------------------------------------------------------

        if include_processed:
            processed_data = self._load_processed_data(
                assets=assets,
                include_processed=include_processed,
                start=start,
                end=end
            )

            for asset in assets:
                merged_assets[asset] = pd.concat(
                    [merged_assets[asset], processed_data[asset]],
                    axis=1
                )
        # 3. Validate consistency across assets
        if validate:
            validate_assets(merged_assets)

        # 4. Align and concatenate across assets
        panel = align_and_concat(merged_assets, method=alignment)
        # ------------------------------------------------------------
        # NEW: Enforce canonical panel contract
        # ------------------------------------------------------------
        # IMPORTANT:
        # alignment step may return columns as (asset, feature)
        # or without explicit names.
        #
        # We explicitly enforce the canonical structure:
        #   level 0 → feature
        #   level 1 → asset
        #   names   → ["feature", "asset"]
        #
        # This ensures:
        #   - consistent downstream usage
        #   - stable API for research layer
        #   - no dependency on alignment implementation details
        #
        # NOTE:
        # This introduces a small overhead (swaplevel + sort_index),
        # but correctness and explicit structure are prioritized
        # at this stage of the project.
        # ------------------------------------------------------------

        if structure == "multiindex":
            panel = enforce_panel_contract(panel)

        # 5. Apply column structure (flat vs multiindex)
        panel = self._apply_structure(panel, structure)

        # 6. Handle missing values
        panel = self._handle_nans(panel, nan_policy)

        return panel
    
 

    # ============================================================
    # INTERNAL METHODS
    # ============================================================

    def _load_data(
        self,
        assets: List[str],
        families: List[str],
        start: Optional[str],
        end: Optional[str],
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Load feature data for each asset and family.

        Parameters
        ----------
        assets : list[str]
            Asset identifiers.
        families : list[str]
            Feature families.
        start : str, optional
            Start date filter.
        end : str, optional
            End date filter.

        Returns
        -------
        dict
            Nested dictionary:
                asset -> family -> DataFrame
        """

        data = {}

        for asset in assets:
            data[asset] = {}

            for family in families:
                df = self.loader.load_asset_features(
                    family=family,
                    asset=asset
                )

                if start:
                    df = df[df.index >= pd.to_datetime(start)]

                if end:
                    df = df[df.index <= pd.to_datetime(end)]

                data[asset][family] = df

        return data

    # ------------------------------------------------------------

    def _merge_families(
        self,
        asset_data: Dict[str, Dict[str, pd.DataFrame]]
    ) -> Dict[str, pd.DataFrame]:
        """
        Merge feature families into a single DataFrame per asset.

        Parameters
        ----------
        asset_data : dict
            Nested dictionary:
                asset -> family -> DataFrame

        Returns
        -------
        dict
            asset -> merged DataFrame (columns = all features)
        """

        merged = {}

        for asset, family_dict in asset_data.items():
            merged[asset] = pd.concat(family_dict.values(), axis=1)

        return merged
    
    def _load_processed_data(
        self,
        assets: List[str],
        include_processed: List[str],
        start: Optional[str],
        end: Optional[str],
    ) -> Dict[str, pd.DataFrame]:
        """
        Load processed data using metadata-driven mapping.
        """

        processed_data = {}

        # ----------------------------------------
        # VALIDATION (against metadata)
        # ----------------------------------------

        missing = [
            col for col in include_processed
            if col not in self.available_processed_features
        ]

        if missing:
            raise ValueError(f"Unknown processed features: {missing}")

        # ----------------------------------------
        # REVERSE MAP (panel → raw)
        # ----------------------------------------

        reverse_mapping = {
            v: k for k, v in self.processed_feature_map.items()
        }

        # ----------------------------------------
        # LOAD PER ASSET
        # ----------------------------------------

        for asset in assets:

            df_proc = self.processed_loader.load_asset(asset)

            # raw column names
            raw_cols = [reverse_mapping[col] for col in include_processed]

            df_proc = df_proc[raw_cols]

            # date filtering
            if start:
                df_proc = df_proc[df_proc.index >= pd.to_datetime(start)]

            if end:
                df_proc = df_proc[df_proc.index <= pd.to_datetime(end)]

            # rename to panel naming
            df_proc = df_proc.rename(columns=self.processed_feature_map)

            processed_data[asset] = df_proc

        return processed_data
    # ------------------------------------------------------------

    def _apply_structure(
        self,
        panel: pd.DataFrame,
        structure: str
    ) -> pd.DataFrame:
        """
        Apply column structure to the panel.

        Parameters
        ----------
        panel : pd.DataFrame
            Panel with MultiIndex columns (asset, feature).
        structure : str
            Desired output format.

        Returns
        -------
        pd.DataFrame
            Panel with transformed column structure.
        """

        if structure == "multiindex":
            return panel

        elif structure == "flat":
            panel.columns = [
                f"{feature}_{asset}"
                for feature, asset in panel.columns
            ]
            return panel

        else:
            raise ValueError(f"Unknown structure: {structure}")

    # ------------------------------------------------------------

    def _handle_nans(
        self,
        panel: pd.DataFrame,
        nan_policy: str
    ) -> pd.DataFrame:
        """
        Handle missing values in the panel.

        Parameters
        ----------
        panel : pd.DataFrame
            Input panel.
        nan_policy : str
            NaN handling strategy.

        Returns
        -------
        pd.DataFrame
            Panel after NaN handling.
        """

        if nan_policy == "drop":
            return panel.dropna()

        elif nan_policy == "ffill":
            return panel.ffill()

        elif nan_policy == "bfill":
            return panel.bfill()

        elif nan_policy == "keep":
            return panel

        else:
            raise ValueError(f"Unknown nan_policy: {nan_policy}")