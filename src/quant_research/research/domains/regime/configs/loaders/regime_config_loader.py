import json
from pathlib import Path
from quant_research.config.paths import RESEARCH_PATH


BASE_PATH = RESEARCH_PATH /"domains"/ "regime" /"configs"


def load_regime_config(config_name: str) -> dict:
    """
    Loads a regime config by name.

    Example:
        load_regime_config("regime_v1")
    """

    path = BASE_PATH / f"{config_name}.json"

    if not path.exists():
        raise FileNotFoundError(f"Regime config not found: {path}")

    with open(path) as f:
        config = json.load(f)

    return config