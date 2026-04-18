from quant_research.systemic.metadata.registry import FEATURE_SEMANTIC_REGISTRY
from quant_research.systemic.metadata.base_features import BASE_FEATURE_REGISTRY

def _extract_base_feature(feature_name: str) -> str:
    return feature_name.split("_")[0]
def enrich_feature(feature, feature_map):
    """
    Enrich a FeatureInstance with semantic metadata.

    Parameters
    ----------
    feature : FeatureInstance
    feature_map : dict[str, FeatureInstance]
        Already computed features (for DAG resolution)
    """

    # ----------------------------------------
    # VALIDATE TYPE
    # ----------------------------------------
    spec = FEATURE_SEMANTIC_REGISTRY.get(feature.type)

    if spec is None:
        raise ValueError(f"[Enricher] Unknown feature type: {feature.type}")

    # ----------------------------------------
    # TRANSFORM FEATURE (e.g. zscore)
    # ----------------------------------------
    if spec["is_transform"]:

        if not feature.inputs:
            raise ValueError(
                f"[Enricher] Transform feature '{feature.name}' missing inputs"
            )

        parent_name = feature.inputs[0]

        if parent_name not in feature_map:
            raise ValueError(
                f"[Enricher] Parent feature '{parent_name}' not found for '{feature.name}'"
            )

        parent = feature_map[parent_name]

        feature.measure = parent.measure
        feature.operator = parent.operator
        feature.transform = feature.type
        feature.domain = spec["domain"]

        return feature

    # ----------------------------------------
    # BASE SYSTEMIC FEATURE
    # ----------------------------------------

    if not feature.inputs:
        raise ValueError(
            f"[Enricher] Feature '{feature.name}' has no inputs"
        )

    raw_input = feature.inputs[0]

    base_feature = _extract_base_feature(raw_input)

    base_spec = BASE_FEATURE_REGISTRY.get(base_feature)

    if base_spec is None:
        raise ValueError(
            f"[Enricher] Unknown base feature: {base_feature}"
        )

    feature.measure = base_spec["measure"]
    feature.operator = spec["operator"]
    feature.transform = None
    feature.domain = spec["domain"]

    return feature