import hashlib
import json


def compute_fv_hash(dataset_hash: str, config: dict) -> str:
    """
    Computes a unique hash for a feature validation run.

    Based on:
    - dataset_hash (data identity)
    - config (validation parameters)
    """

    config_str = json.dumps(config, sort_keys=True)

    raw = dataset_hash + config_str

    return hashlib.md5(raw.encode()).hexdigest()