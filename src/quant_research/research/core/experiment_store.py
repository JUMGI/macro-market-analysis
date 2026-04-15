import json
from pathlib import Path
from quant_research.config.paths import RESEARCH_DATA_PATH
BASE_PATH = RESEARCH_DATA_PATH / "experiments"


def get_experiment_path(experiment_hash: str) -> Path:
    return BASE_PATH / experiment_hash


def experiment_exists(experiment_hash: str) -> bool:
    return get_experiment_path(experiment_hash).exists()


def save_experiment(
    experiment_hash: str,
    config: dict,
    metrics: dict,
    score: dict,
    selected_features,
    fv_metadata,
    regime_df
):

    path = get_experiment_path(experiment_hash)
    path.mkdir(parents=True, exist_ok=True)

    assert hasattr(fv_metadata, "fv_hash"), "fv_metadata must be FeatureMetadata"

    # 🔹 config
    with open(path / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # 🔹 metrics
    payload = {
        "experiment_hash": experiment_hash,
        "metrics": metrics,
        "score": score
    }

    with open(path / "metrics.json", "w") as f:
        json.dump(payload, f, indent=2)

    summary = {
        "experiment_hash": experiment_hash,
        "dataset_id": config["dataset"]["id"],
        "fv_hash": fv_metadata.fv_hash,
        "n_features": len(selected_features),
        "score": score["total"]
    }

    with open(path / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # 🔹 regime output
    regime_df.to_parquet(path / "regime.parquet")

def should_run(experiment_hash: str) -> bool:
    return not experiment_exists(experiment_hash)