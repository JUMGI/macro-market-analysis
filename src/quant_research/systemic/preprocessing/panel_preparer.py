import pandas as pd


class PanelPreparer:

    def __init__(self, config: dict):
        self.config = config

    def prepare(self, panel: pd.DataFrame):

        nan_cfg = self.config["nan_handling"]

        panel_work = panel.copy()

        # -------------------------
        # 1. FEATURE FILTER (opcional)
        # -------------------------

        required_features = self._extract_required_features()

        if nan_cfg["warmup"]["based_on"] == "used_features":
            panel_work = panel_work.loc[:, panel_work.columns.get_level_values(0).isin(required_features)]

        # -------------------------
        # 2. WARMUP
        # -------------------------

        warmup_start = None

        if nan_cfg["warmup"]["method"] == "cut":
            first_valid = panel_work.apply(lambda col: col.first_valid_index())
            warmup_start = max(first_valid)
            panel_work = panel_work.loc[panel_work.index >= warmup_start]

        # -------------------------
        # 3. CALENDAR
        # -------------------------

        method = nan_cfg["calendar"]["method"]

        if method == "ffill":
            panel_work = panel_work.ffill()
        elif method == "bfill":
            panel_work = panel_work.bfill()
        elif method == "drop":
            panel_work = panel_work.dropna()

        return panel_work, {
            "warmup_start": str(warmup_start) if warmup_start else None,
            "features_used": required_features
        }

    # -------------------------
    # HELPERS
    # -------------------------

    def _extract_required_features(self):

        features = []

        for f in self.config.get("features", {}).values():
            for v in f.values():
                features.append(v)

        features.append("RET_1")

        return list(set(features))