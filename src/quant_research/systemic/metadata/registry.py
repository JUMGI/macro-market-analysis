FEATURE_SEMANTIC_REGISTRY = {
    "mean": {
        "operator": "mean",
        "domain": "cross_sectional",
        "is_transform": False
    },
    "dispersion": {
        "operator": "dispersion",
        "domain": "cross_sectional",
        "is_transform": False
    },
    "breadth": {
        "operator": "breadth",
        "domain": "cross_sectional",
        "is_transform": False
    },
    "correlation": {
        "operator": "correlation",
        "domain": "cross_sectional",
        "is_transform": False
    },
    "range": {
        "operator": "range",
        "domain": "cross_sectional",
        "is_transform": False
    },
    "zscore": {
        "operator": None,   # hereda
        "domain": "temporal",
        "is_transform": True
    }
}