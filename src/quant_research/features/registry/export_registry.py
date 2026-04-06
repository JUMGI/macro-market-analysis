import json
import hashlib
import pandas as pd


def export_feature_registry_snapshot(
    registry,
    output_path,
):
    """
    Export a static snapshot of the feature registry.

    This represents:
    - what features the system can compute
    - independent of data availability
    """

    # ----------------------------------------
    # DESCRIBE FEATURES
    # ----------------------------------------

    features = registry.describe_expanded()

    # ----------------------------------------
    # NORMALIZE (IMPORTANT FOR HASH)
    # ----------------------------------------

    features_sorted = sorted(features, key=lambda x: x["name"])

    # ----------------------------------------
    # HASH (registry version)
    # ----------------------------------------

    registry_hash = hashlib.md5(
        json.dumps(features_sorted, sort_keys=True).encode()
    ).hexdigest()

    # ----------------------------------------
    # METADATA OBJECT
    # ----------------------------------------

    metadata = {
        "layer": "features",

        "created_at": pd.Timestamp.now().isoformat(),

        # --- registry content
        "n_features": len(features_sorted),
        "features": features_sorted,

        # --- versioning
        "registry_hash": registry_hash,
    }

    # ----------------------------------------
    # SAVE
    # ----------------------------------------

    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=4)