"""
Feature Registry Helpers
------------------------

Utilities to work with the feature registry.

Responsibilities:

- flatten the registry
- list families
- list groups within families
- retrieve feature lists
- validate feature names

These helpers allow the research layer
to interact cleanly with the feature registry.
"""

from quant_research.features.registry.asset_feature_registry import ASSET_FEATURE_REGISTRY


# ============================================================
# Flatten Registry
# ============================================================

def flatten_registry():

    """
    Return a flat list with all features in the registry.
    """

    features = []

    for family in ASSET_FEATURE_REGISTRY.values():

        for group in family.values():

            features.extend(group)

    return sorted(set(features))


# ============================================================
# List Families
# ============================================================

def list_families():

    """
    Return available feature families.
    """

    return list(ASSET_FEATURE_REGISTRY.keys())


# ============================================================
# List Groups
# ============================================================

def list_groups(family):

    """
    Return groups inside a feature family.
    """

    if family not in ASSET_FEATURE_REGISTRY:
        raise ValueError(f"Unknown family: {family}")

    return list(ASSET_FEATURE_REGISTRY[family].keys())


# ============================================================
# Get Features
# ============================================================

def get_features(family=None, group=None):

    """
    Retrieve features from registry.

    Parameters
    ----------
    family : str
        Feature family (momentum, volatility)

    group : str
        Feature group within family

    Returns
    -------
    list
        List of feature names
    """

    if family is None:
        return flatten_registry()

    if family not in ASSET_FEATURE_REGISTRY:
        raise ValueError(f"Unknown family: {family}")

    if group is None:

        features = []

        for g in ASSET_FEATURE_REGISTRY[family].values():
            features.extend(g)

        return sorted(set(features))

    if group not in ASSET_FEATURE_REGISTRY[family]:
        raise ValueError(f"Unknown group: {group}")

    return ASSET_FEATURE_REGISTRY[family][group]


# ============================================================
# Feature Validation
# ============================================================

def validate_feature(feature_name):

    """
    Check if a feature exists in the registry.
    """

    all_features = flatten_registry()

    return feature_name in all_features
