# src/quant_research/features/registry/asset_feature_registry.py

"""
asset_feature_registry.py

Central registry for asset-level features. Automatically registers all
momentum and volatility features using dynamic builders.

Provides:
- Access by feature name
- Access by family
- List of all registered features
- Ready-to-use compute functions for each feature
"""

from typing import List
from .feature_spec import FeatureSpec
from .build_features import build_momentum_features_spec, build_volatility_features_spec

class FeatureRegistry:
    """
    Central registry of asset-level features.
    """

    def __init__(self):
        self._features = {}  # name -> FeatureSpec
        self._bootstrap()

    def _bootstrap(self):
        """
        Automatically populate the registry using the dynamic builders.
        """
        for f in build_momentum_features_spec() + build_volatility_features_spec():
            self.register(f)

    def register(self, feature: FeatureSpec):
        """
        Register a single FeatureSpec. Overwrites if the feature already exists.
        """
        self._features[feature.name] = feature

    def get(self, name: str) -> FeatureSpec:
        """
        Retrieve a FeatureSpec by its name.
        """
        return self._features[name]

    def list(self) -> List[str]:
        """
        List all registered feature names.
        """
        return list(self._features.keys())

    def get_many(self, names: List[str]) -> List[FeatureSpec]:
        """
        Retrieve multiple FeatureSpec objects by name.
        """
        return [self._features[n] for n in names]

    def get_by_family(self, family: str) -> List[FeatureSpec]:
        """
        Retrieve all FeatureSpec objects belonging to a given family.
        """
        return [f for f in self._features.values() if f.family == family]


# Singleton instance of the registry
registry = FeatureRegistry()