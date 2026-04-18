from typing import Dict, Any, List


class GroupDefinition:

    def __init__(self, name: str, conditions: Dict[str, Any]):
        self.name = name
        self.conditions = conditions

    def matches(self, feature_info: Dict[str, Any], context: Dict[str, Any]) -> bool:

        for k, v in self.conditions.items():

            if k in feature_info:
                if feature_info.get(k) != v:
                    return False

            elif k in context:
                if context.get(k) != v:
                    return False

            else:
                return False

        return True


GROUP_REGISTRY: List[GroupDefinition] = [

    # -------------------------
    # MOMENTUM
    # -------------------------

    GroupDefinition(
        name="mom_mean_raw",
        conditions={
            "measure": "momentum",
            "operator": "mean",
            "transform": None,
            "input_type": "raw"
        }
    ),

    GroupDefinition(
        name="mom_mean_from_z",
        conditions={
            "measure": "momentum",
            "operator": "mean",
            "transform": None,
            "input_type": "normalized"
        }
    ),

    GroupDefinition(
        name="mom_mean_zscore",
        conditions={
            "measure": "momentum",
            "operator": "mean",
            "transform": "zscore"
        }
    ),

    GroupDefinition(
        name="mom_dispersion_from_z",
        conditions={
            "measure": "momentum",
            "operator": "dispersion",
            "input_type": "normalized"
        }
    ),

    GroupDefinition(
        name="mom_breadth_from_z",
        conditions={
            "measure": "momentum",
            "operator": "breadth",
            "input_type": "normalized"
        }
    ),

    GroupDefinition(
        name="mom_corr_from_z",
        conditions={
            "measure": "momentum",
            "operator": "correlation",
            "input_type": "normalized"
        }
    ),

    GroupDefinition(
        name="mom_range_from_z",
        conditions={
            "measure": "momentum",
            "operator": "range",
            "input_type": "normalized"
        }
    ),

    # -------------------------
    # RETURNS
    # -------------------------

    GroupDefinition(
        name="ret_mean_raw",
        conditions={
            "measure": "returns",
            "operator": "mean",
            "input_type": "raw"
        }
    ),

    # -------------------------
    # VOLATILITY
    # -------------------------

    GroupDefinition(
        name="vol_mean_from_z",
        conditions={
            "measure": "volatility",
            "operator": "mean",
            "input_type": "normalized"
        }
    ),

    # -------------------------
    # RETURNS (normalized fallback)
    # -------------------------

    GroupDefinition(
        name="ret_mean_from_z",
        conditions={
            "measure": "returns",
            "operator": "mean",
            "input_type": "normalized"
        }
    ),

    # -------------------------
    # VOLATILITY (raw fallback)
    # -------------------------

    GroupDefinition(
        name="vol_mean_raw",
        conditions={
            "measure": "volatility",
            "operator": "mean",
            "input_type": "raw"
        }
    ),

    # -------------------------
    # MOMENTUM (raw fallbacks)
    # -------------------------

    GroupDefinition(
        name="mom_dispersion_raw",
        conditions={
            "measure": "momentum",
            "operator": "dispersion",
            "input_type": "raw"
        }
    ),

    GroupDefinition(
        name="mom_breadth_raw",
        conditions={
            "measure": "momentum",
            "operator": "breadth",
            "input_type": "raw"
        }
    ),

    GroupDefinition(
        name="mom_range_raw",
        conditions={
            "measure": "momentum",
            "operator": "range",
            "input_type": "raw"
        }
    ),
]