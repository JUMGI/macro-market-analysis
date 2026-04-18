import pandas as pd
from quant_research.systemic.aggregators import AGGREGATOR_REGISTRY



class SystemicBuilder:

    def __init__(self, features):
        self.features = features

       # print("\n[CONFIG EXPANDED]")
       # for c in features:
       #     print(c)




    # ============================================================
    # PUBLIC
    # ============================================================

    def build(self, panel):

        outputs = {}

        for feature in self.features:

            if feature.inputs and feature.inputs[0] in outputs:
                data = outputs[feature.inputs[0]]
            else:
                data = self._extract_features(panel, feature.inputs)

            func = AGGREGATOR_REGISTRY[feature.type]
            outputs[feature.name] = func(data, **feature.params)

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


    
