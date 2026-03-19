# src/quant_research/features/registry/asset_feature_registry.py

from typing import List
from quant_research.features.registry.feature_spec import FeatureSpec
from quant_research.features.registry.build_features import (
    build_momentum_features_spec,
    build_volatility_features_spec,
)
from pathlib import Path


class FeatureRegistry:
    """
    Central registry of asset-level features.
    """

    def __init__(self, base_path: Path):
        self._features = {}  # name -> FeatureSpec
        self._bootstrap(base_path)

    def _bootstrap(self, base_path: Path):
    
        "Automatically populate the registry using the dynamic builders."
   
        specs = (
            build_momentum_features_spec() +
            build_volatility_features_spec()
        )

        for f in specs:
            self.register(f)

    def register(self, feature: FeatureSpec):
        """
        Register a single FeatureSpec. Overwrites if the feature already exists.
        """
        self._features[feature.name] = feature

    def get(self, name: str) -> FeatureSpec:
        return self._features[name]

    def list(self) -> List[str]:
        return list(self._features.keys())

    def get_many(self, names: List[str]) -> List[FeatureSpec]:
        return [self._features[n] for n in names]

    def get_by_family(self, family: str) -> List[FeatureSpec]:
        return [f for f in self._features.values() if f.family == family]


# ============================================================
# Singleton
# ============================================================

def create_registry(base_path: Path) -> FeatureRegistry:
    return FeatureRegistry(base_path)