import json
from pathlib import Path

from quant_research.config.paths import PROJECT_ROOT
def load_validation_config(name: str) -> dict:
    path = Path(PROJECT_ROOT / "src/quant_research/feature_validation/configs") / f"{name}.json"

    with open(path) as f:
        return json.load(f)