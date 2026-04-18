import json
from pathlib import Path
from quant_research.config.paths import RESEARCH_DATA_PATH

BASE_PATH = RESEARCH_DATA_PATH / "experiments"


# -------------------------
# PATHS
# -------------------------

def get_experiment_path(experiment_hash: str) -> Path:
    return BASE_PATH / experiment_hash


def experiment_exists(experiment_hash: str) -> bool:
    return get_experiment_path(experiment_hash).exists()


def should_run(experiment_hash: str) -> bool:
    return not experiment_exists(experiment_hash)


# -------------------------
# SAVE (NEW API)
# -------------------------

def save_experiment(
    experiment_hash: str,
    artifact: dict
):
    """
    Guarda un experiment artifact completo.
    """

    path = get_experiment_path(experiment_hash)
    path.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # 1. FULL ARTIFACT
    # -------------------------
    with open(path / "artifact.json", "w") as f:
        json.dump(artifact, f, indent=2)

    # -------------------------
    # 2. SUMMARY (FAST ACCESS)
    # -------------------------
    best = artifact["execution"]["best_result"]

    summary = {
        "experiment_hash": experiment_hash,
        "dataset_id": artifact["identity"]["dataset_id"],
        "dataset_hash": artifact["identity"]["dataset_hash"],
        "fv_hash": artifact["identity"]["fv_hash"],
        "n_samples": artifact["execution"]["n_samples"],
        "score": best["score"]["total"]
    }

    with open(path / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # -------------------------
    # 3. BEST RESULT MATERIALIZATION
    # -------------------------
    best_path = path / "best"
    best_path.mkdir(exist_ok=True)

    # config usado
    with open(best_path / "config.json", "w") as f:
        json.dump(best["regime_config"], f, indent=2)

    # regime output (si existe)
    #if "regime_df" in best:
       # best["regime_df"].to_parquet(best_path / "regime.parquet")


def load_experiment(experiment_hash: str) -> dict:
    path = get_experiment_path(experiment_hash)

    with open(path / "artifact.json") as f:
        return json.load(f)