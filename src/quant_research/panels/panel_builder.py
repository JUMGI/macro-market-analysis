from typing import List, Optional
import pandas as pd


class PanelBuilder:

    def __init__(self, feature_loader):
        self.loader = feature_loader

    def build_panel(
        self,
        assets: List[str],
        families: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
        alignment: str = "union",
        nan_policy: str = "keep",
        structure: str = "multiindex"
    ) -> pd.DataFrame:

        asset_data = self._load_data(assets, families, start=start, end=end)
        merged_assets = self._merge_families(asset_data)
        panel = self._merge_assets(merged_assets, alignment)
        panel = self._apply_structure(panel, structure)
        panel = self._handle_nans(panel, nan_policy)

        self._log_panel(panel, assets, families, alignment)

        return panel

    # =========================================
    def _log_panel(self, panel, assets, families, alignment):

        n_rows, n_cols = panel.shape

        nan_pct = panel.isna().mean().mean() * 100

        date_min = panel.index.min()
        date_max = panel.index.max()

        print("\n=== PANEL BUILT ===")
        print(f"Assets: {assets}")
        print(f"Families: {families}")
        print(f"Shape: {n_rows} rows x {n_cols} columns")
        print(f"Date range: {date_min} → {date_max}")
        print(f"NaN %: {nan_pct:.2f}%")
        print(f"Alignment: {alignment}")
        print("====================\n")

    def _load_data(
        self,
        assets: List[str],
        families: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None
    ):

        data = {}

        for asset in assets:
            data[asset] = {}

            for family in families:

                # 👇 loader SIMPLE (sin start/end)
                df = self.loader.load_asset_features(
                    family=family,
                    asset=asset
                )

                # 👇 filtrado SOLO si corresponde
                if start is not None:
                    start_dt = pd.to_datetime(start)
                    df = df[df.index >= start_dt]

                if end is not None:
                    end_dt = pd.to_datetime(end)
                    df = df[df.index <= end_dt]

                data[asset][family] = df

        return data

    # =========================================

    def _merge_families(self, asset_data):

        merged = {}

        for asset, family_dict in asset_data.items():
            dfs = list(family_dict.values())
            merged[asset] = pd.concat(dfs, axis=1)

        return merged

    # =========================================

    def _merge_assets(self, merged_assets, alignment):

        join_type = "inner" if alignment == "intersection" else "outer"

        panel = pd.concat(
            merged_assets,
            axis=1,
            join=join_type
        )

        return panel

    # =========================================

    def _apply_structure(self, panel, structure):

        if structure == "multiindex":
            return panel

        elif structure == "flat":
            panel.columns = [
                f"{asset}_{feature}"
                for asset, feature in panel.columns
            ]
            return panel

        else:
            raise ValueError(f"Unknown structure: {structure}")

    # =========================================

    def _handle_nans(self, panel, nan_policy):

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