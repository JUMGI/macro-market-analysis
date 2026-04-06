import json
import hashlib
import pandas as pd


class FeatureCatalogBuilder:

    def __init__(
        self,
        processed_metadata_path,
        registry_snapshot_path,
    ):
        self.processed_metadata_path = processed_metadata_path
        self.registry_snapshot_path = registry_snapshot_path

    # ============================================================
    # PUBLIC
    # ============================================================

    def build(self):

        processed = self._load_json(self.processed_metadata_path)
        registry = self._load_json(self.registry_snapshot_path)

        catalog = self._merge(processed, registry)

        return catalog

    # ============================================================
    # LOADERS
    # ============================================================

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    # ============================================================
    # MERGE LOGIC
    # ============================================================

    def _merge(self, processed, registry):

        processed_features = set(processed["features"])
        registry_features = registry["features"]

        catalog_features = []

        # ----------------------------------------
        # 1. PRIMITIVE FEATURES (from processed)
        # ----------------------------------------

        for f in processed_features:
            catalog_features.append({
                "name": f,
                "source": "processed",
                "family": "primitive",
                "inputs": [],
                "available": True,
            })

        # ----------------------------------------
        # 2. COMPUTABLE FEATURES (from registry)
        # ----------------------------------------

        for f in registry_features:

            name = f["name"]

            # skip if already primitive
            if name in processed_features:
                continue

            catalog_features.append({
                "name": name,
                "source": "feature_pipeline",
                "family": f["family"],
                "inputs": f["inputs"],
                "available": False,  # requires compute
            })

        # ----------------------------------------
        # HASH
        # ----------------------------------------

        catalog_sorted = sorted(catalog_features, key=lambda x: x["name"])

        catalog_hash = hashlib.md5(
            json.dumps(catalog_sorted, sort_keys=True).encode()
        ).hexdigest()

        # ----------------------------------------
        # FINAL OBJECT
        # ----------------------------------------

        return {
            "created_at": pd.Timestamp.now().isoformat(),

            "n_features": len(catalog_sorted),

            "features": catalog_sorted,

            "hash": catalog_hash,

            "sources": {
                "processed_hash": processed.get("config_hash"),
                "registry_hash": registry.get("registry_hash"),
            }
        }