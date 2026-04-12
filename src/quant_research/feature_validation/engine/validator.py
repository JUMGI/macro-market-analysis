from typing import Dict
import pandas as pd

from quant_research.feature_validation.models.metadata import FeatureMetadata
from quant_research.feature_validation.utils.hash import compute_fv_hash

class FeatureValidator:

    def __init__(self, profile, dataset_id: str, dataset_hash: str, config: Dict = None):
        self.profile = profile
        self.dataset_id = dataset_id
        self.dataset_hash = dataset_hash
        self.config = config or {}

    def validate(self, features: pd.DataFrame) -> FeatureMetadata:

        fv_hash = compute_fv_hash(
        dataset_hash=self.dataset_hash,
        config=self.config
        )

        results = {}

        for col in features.columns:
            series = features[col]

            try:
                results[col] = self.profile.evaluate(series, features)

            except Exception as e:
                # importante para robustness
                results[col] = {
                    "error": str(e)
                }

        metadata = FeatureMetadata(
            dataset_id=self.dataset_id,
            dataset_hash=self.dataset_hash,
            fv_hash=fv_hash,
            profile=self.profile.__class__.__name__,
            config=self.config,
            metrics=results
            
        )

        return metadata