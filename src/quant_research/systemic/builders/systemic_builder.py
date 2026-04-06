import pandas as pd
from quant_research.systemic.aggregators import AGGREGATOR_REGISTRY
from quant_research.systemic.config.config_expander import SystemicConfigExpander

class SystemicBuilder:

    def __init__(self, configs):

        # ----------------------------------------
        # EXPAND CONFIG
        # ----------------------------------------
        expander = SystemicConfigExpander(configs)
        self.configs = expander.expand()

        print("\n[CONFIG EXPANDED]")
        for c in self.configs:
            print(c)

    # ============================================================
    # PUBLIC
    # ============================================================

    def build(self, panel: pd.DataFrame) -> pd.DataFrame:

        if not isinstance(panel.columns, pd.MultiIndex):
            raise ValueError("Panel must have MultiIndex columns")
        
        configs = self.configs

        outputs = {}

        for cfg in configs:

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

            params = cfg.get("params", {})
                

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


    
    def _expand_config(self):
        
        expanded = []

        for cfg in self.config:

            params = cfg.get("params")

            # caso simple (sin expansión)
            if not params:
                expanded.append(cfg)
                continue

            # detectar listas en params
            keys = []
            values = []

            for k, v in params.items():
                if isinstance(v, list):
                    keys.append(k)
                    values.append(v)
                else:
                    keys.append(k)
                    values.append([v])

            # generar combinaciones
            import itertools

            for combo in itertools.product(*values):
                new_cfg = cfg.copy()

                combo_dict = dict(zip(keys, combo))

                # expandir nombre
                suffix = "_".join(str(v) for v in combo_dict.values())
                new_cfg["name"] = f"{cfg['name']}_{suffix}"

                # expandir features
                new_features = []
                for f in cfg.get("features", []):
                    new_features.append(f.format(**combo_dict))

                new_cfg["features"] = new_features

                # reemplazar params por valores concretos
                for k, v in combo_dict.items():
                    new_cfg[k] = v

                new_cfg.pop("params", None)

                expanded.append(new_cfg)
        return expanded