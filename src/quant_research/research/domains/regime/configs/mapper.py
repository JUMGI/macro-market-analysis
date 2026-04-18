import copy


def _resolve_value(obj, sample):
    """
    Resuelve cualquier estructura que contenga:
    {"param": "..."} → valor real desde sample["params"]
    """

    # caso base: dict param
    if isinstance(obj, dict):

        if "param" in obj:
            param_name = obj["param"]
            return sample["params"][param_name]

        # recurse
        return {
            k: _resolve_value(v, sample)
            for k, v in obj.items()
        }

    # listas
    elif isinstance(obj, list):
        return [_resolve_value(x, sample) for x in obj]

    # valores normales
    return obj


def _resolve_features(config, sample):
    """
    Reemplaza features abstractas por features concretas
    SOLO en conditions (no tocar otras cosas)
    """

    for regime in config["model"]["regimes"]:
        for rule in regime["rules"]:
            for cond in rule["conditions"]:

                feature_key = cond.get("feature")

                if feature_key in sample["features"]:
                    cond["feature"] = sample["features"][feature_key]

    return config


def map_features(base_config: dict, sample: dict) -> dict:
    """
    Pipeline completo:
    1. reemplazar features
    2. resolver params en todo el config
    """

    config = copy.deepcopy(base_config)

    # -------------------------
    # 1. Resolve features
    # -------------------------
    config = _resolve_features(config, sample)

    # -------------------------
    # 2. Resolve params (global)
    # -------------------------
    config = _resolve_value(config, sample)

    return config