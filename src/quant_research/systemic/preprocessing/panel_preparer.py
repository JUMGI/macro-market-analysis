import pandas as pd

class PanelPreparer:

    def __init__(self, nan_config: dict):
        self.nan_config = nan_config

    # ------------------------------------------------------------

    def prepare(
        self,
        panel: pd.DataFrame,
        required_features: list
    ):

        panel_work = panel.copy()

        # -------------------------
        # 1. FILTER FEATURES 🔥
        # -------------------------

        panel_work = panel_work.loc[
            :,
            panel_work.columns.get_level_values(0).isin(required_features)
        ]

        # -------------------------
        # 2. WARMUP
        # -------------------------

        warmup_cfg = self.nan_config["warmup"]

        warmup_start = None

        if warmup_cfg["method"] == "cut":

            first_valid = panel_work.apply(
                lambda col: col.first_valid_index()
            )

            warmup_start = max(first_valid)

            panel_work = panel_work.loc[
                panel_work.index >= warmup_start
            ]

        # -------------------------
        # 3. CALENDAR
        # -------------------------

        method = self.nan_config["calendar"]["method"]

        if method == "ffill":
            panel_work = panel_work.ffill()
        elif method == "bfill":
            panel_work = panel_work.bfill()
        elif method == "drop":
            panel_work = panel_work.dropna()

        # -------------------------
        # 4. FINAL
        # -------------------------

        final_method = self.nan_config["final"]["method"]

        if final_method == "dropna":
            panel_work = panel_work.dropna()

        return panel_work, {
            "features_used": required_features,
            "warmup_start": str(warmup_start) if warmup_start else None
        }