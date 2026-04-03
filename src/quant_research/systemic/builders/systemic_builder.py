import pandas as pd
from quant_research.systemic.aggregators import AGGREGATOR_REGISTRY


class SystemicBuilder:
    """
    Build systemic features from a panel (feature, asset).
    """

    def __init__(self, config: list[dict]):
        self.config = config

    # ============================================================
    # PUBLIC
    # ============================================================

    def build(self, panel: pd.DataFrame) -> pd.DataFrame:

        if not isinstance(panel.columns, pd.MultiIndex):
            raise ValueError("Panel must have MultiIndex columns")

        outputs = {}

        for cfg in self.config:

            name = cfg["name"]
            ftype = cfg["type"]

            # ----------------------------------------
            # INPUT
            # ----------------------------------------

            if "input" in cfg:
                data = outputs[cfg["input"]]

            else:
                features = cfg.get("features", [])
                data = self._extract_features(panel, features)

            # ----------------------------------------
            # PARAMS
            # ----------------------------------------

            params = self._extract_params(
                cfg,
                exclude=["name", "type", "features", "input"]
            )

            # ----------------------------------------
            # APPLY
            # ----------------------------------------

            func = AGGREGATOR_REGISTRY[ftype]
            result = func(data, **params)

            outputs[name] = result

        return pd.DataFrame(outputs)

    # ============================================================
    # INTERNALS
    # ============================================================

    def _extract_features(
        self,
        panel: pd.DataFrame,
        features: list[str]
    ) -> pd.DataFrame:
        """
        Extract features and return flat DataFrame (assets as columns)
        """

        if not features:
            raise ValueError("No features specified")

        mask = panel.columns.get_level_values("feature").isin(features)
        df = panel.loc[:, mask]

        if df.shape[1] == 0:
            raise ValueError(f"No columns found for features: {features}")

        # 🔥 CLAVE: flatten a columnas = assets
        df = df.copy()
        df.columns = df.columns.get_level_values("asset")

        return df

    def _extract_params(self, cfg: dict, exclude: list[str]) -> dict:
        return {k: v for k, v in cfg.items() if k not in exclude}