import json
import hashlib
from datetime import datetime


class RegimeMetadataBuilder:

    def build(self, regime_df, config: dict, systemic_metadata: dict) -> dict:

        model_cfg = config.get("model", {})
        proc_cfg = config.get("processors", [])

        # -------------------------
        # HASHES
        # -------------------------

        model_hash = self._hash_dict(model_cfg)
        proc_hash = self._hash_dict(proc_cfg)

        full_hash = self._hash_dict({
            "model": model_cfg,
            "processors": proc_cfg
        })

        # -------------------------
        # FEATURES
        # -------------------------

        used_features = sorted(self._extract_features(config))
        available_features = set(
            systemic_metadata.get("systemic", {}).get("features", [])
        )

        missing_features = sorted(set(used_features) - available_features)

        # -------------------------
        # MODEL INFO
        # -------------------------

        regimes = self._extract_regime_names(model_cfg)

        # -------------------------
        # BUILD METADATA
        # -------------------------

        metadata = {
            "name": config.get("name", "unnamed_regime"),
            "created_at": datetime.utcnow().isoformat(),

            "pipeline": {
                "model": model_cfg.get("type"),
                "processors": [p.get("type") for p in proc_cfg],
                "version": "v1"
            },

            "config_hash": full_hash,

            "model": {
                "type": model_cfg.get("type"),
                "config_hash": model_hash,
                "n_regimes": len(regimes),
                "regimes": regimes
            },

            "processing": {
                "config_hash": proc_hash,
                "steps": proc_cfg
            },

            "features": {
                "used": used_features,
                "missing": missing_features
            },

            "systemic": {
                "name": systemic_metadata.get("name"),
                "dataset_hash": systemic_metadata.get("dataset_hash"),
                "config_hash": systemic_metadata.get("config_hash"),
                "n_features": systemic_metadata.get("systemic", {}).get("n_features"),
                "date_range": systemic_metadata.get("date_range")
            }
        }
        metadata["model_config_hash"] = model_hash
        metadata["processing_config_hash"] = proc_hash

        return metadata

    # =========================================================
    # INTERNALS
    # =========================================================

    def _hash_dict(self, d: dict) -> str:
        """
        Stable hash for dicts/lists (order-independent)
        """
        s = json.dumps(d, sort_keys=True)
        return hashlib.md5(s.encode()).hexdigest()

    # -------------------------

    def _extract_features(self, config: dict) -> set:
        """
        Extract features from rule-based config.
        Compatible with list or dict regimes.
        """

        features = set()

        model_cfg = config.get("model", {})
        regimes = model_cfg.get("regimes", [])

        # soporta list o dict
        if isinstance(regimes, dict):
            regimes_iter = regimes.values()
        else:
            regimes_iter = regimes

        for regime in regimes_iter:
            for rule in regime.get("rules", []):
                for cond in rule.get("conditions", []):

                    feature = cond.get("feature")

                    if feature:
                        features.add(feature)

        return features

    # -------------------------

    def _extract_regime_names(self, model_cfg: dict):

        regimes = model_cfg.get("regimes", [])

        if isinstance(regimes, dict):
            return list(regimes.keys())

        return [r.get("name") for r in regimes if "name" in r]