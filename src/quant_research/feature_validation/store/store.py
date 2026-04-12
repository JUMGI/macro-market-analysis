import json
from pathlib import Path
from quant_research.config.paths import FEATURE_VALIDATION_PATH

class FeatureValidationStore:

    BASE_PATH = FEATURE_VALIDATION_PATH

    @classmethod
    def save(cls, metadata):

        path = cls.BASE_PATH / metadata.dataset_id
        path.mkdir(parents=True, exist_ok=True)

        file = path / f"{metadata.version}.json"

        with open(file, "w") as f:
            json.dump(metadata.__dict__, f, indent=4)

    @classmethod
    def load(cls, dataset_id: str, version: str):

        file = cls.BASE_PATH / dataset_id / f"{version}.json"

        with open(file) as f:
            data = json.load(f)

        return data