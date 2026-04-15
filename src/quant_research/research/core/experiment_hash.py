import json
import hashlib


def compute_experiment_hash(config, dataset_metadata, fv_metadata):

    payload = {
        "dataset_hash": dataset_metadata["dataset_hash"],
        "fv_hash": fv_metadata.fv_hash,
        "feature_selection": config.get("feature_selection"),
        "regime": config.get("regime_config_full"),
        "evaluation": config.get("evaluation"),
    }

    payload_str = json.dumps(payload, sort_keys=True)

    return hashlib.sha256(payload_str.encode()).hexdigest()