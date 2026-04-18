from itertools import product
import copy
from quant_research.systemic.features.feature_instance import FeatureInstance

class SystemicConfigExpander:

    def __init__(self, configs):
        self.configs = configs

    def expand(self):

        expanded = []

        for cfg in self.configs:

            # ----------------------------------------
            # NO EXPANSION → PASA DIRECTO
            # ----------------------------------------
            if "expand" not in cfg:
                inputs = []

                if "input" in cfg:
                    inputs = [cfg["input"]]

                elif "features" in cfg:
                    inputs = cfg["features"]

                params = cfg.get("params", {})

                feature = FeatureInstance(
                    name=cfg["name"],
                    type_=cfg["type"],
                    params=params,
                    inputs=inputs
                )

                expanded.append(feature)
                continue
               

            expand_dict = cfg["expand"]

            # VALIDACIÓN (🔥 importante)
            for k, v in expand_dict.items():
                if not isinstance(v, (list, tuple)):
                    raise ValueError(
                        f"Expand param '{k}' must be a list, got {type(v)}"
                    )

            keys = list(expand_dict.keys())
            values = list(expand_dict.values())

            for combo in product(*values):

                param_dict = dict(zip(keys, combo))
                new_cfg = copy.deepcopy(cfg)

                # ----------------------------------------
                # helper: formatear strings
                # ----------------------------------------
                def format_value(v):
                    if isinstance(v, str):
                        formatted = v.format(**param_dict)

                        # 🔥 intentar convertir a número
                        if formatted.isdigit():
                            return int(formatted)

                        try:
                            return float(formatted)
                        except ValueError:
                            return formatted

                    return v

                # ----------------------------------------
                # NAME
                # ----------------------------------------
                new_cfg["name"] = format_value(new_cfg["name"])

                # ----------------------------------------
                # FEATURES
                # ----------------------------------------
                if "features" in new_cfg:
                    new_cfg["features"] = [
                        format_value(f) for f in new_cfg["features"]
                    ]

                # ----------------------------------------
                # INPUT (DAG)
                # ----------------------------------------
                if "input" in new_cfg:
                    new_cfg["input"] = format_value(new_cfg["input"])

                # ----------------------------------------
                # PARAMS (🔥 clave)
                # ----------------------------------------
                if "params" in new_cfg:
                    new_cfg["params"] = {
                        k: format_value(v)
                        for k, v in new_cfg["params"].items()
                    }

                # ----------------------------------------
                # CLEAN
                # ----------------------------------------
                del new_cfg["expand"]

                # ----------------------------------------
                # BUILD FEATURE INSTANCE
                # ----------------------------------------

                inputs = []

                if "input" in new_cfg:
                    inputs = [new_cfg["input"]]

                elif "features" in new_cfg:
                    inputs = new_cfg["features"]

                params = new_cfg.get("params", {})

                feature = FeatureInstance(
                    name=new_cfg["name"],
                    type_=new_cfg["type"],
                    params=params,
                    inputs=inputs
                )

                expanded.append(feature)

        return expanded