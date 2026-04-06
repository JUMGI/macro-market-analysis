from typing import List, Dict
from quant_research.features.registry.feature_spec import FeatureSpec
from quant_research.features.registry.build_features import build_all_feature_specs


class FeatureRegistry:
    """
    Central registry of feature specifications (agent-ready).

    - Data-independent
    - Declarative
    - Supports discovery, filtering, and execution
    """

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self):
        self._features: Dict[str, FeatureSpec] = {}
        self._bootstrap()

    # ============================================================
    # Bootstrap
    # ============================================================

    def _bootstrap(self):
        """
        Populate registry from builders (declarative, no data dependency).
        """

        specs = build_all_feature_specs()

        for spec in specs:
            self.register(spec)

    # ============================================================
    # Core API
    # ============================================================

    def register(self, feature: FeatureSpec):
        """
        Register a FeatureSpec.
        Overwrites if name already exists.
        """
        self._features[feature.name] = feature

    def get(self, name: str) -> FeatureSpec:
        """
        Get a feature by name.
        """
        if name not in self._features:
            raise KeyError(f"Feature '{name}' not found in registry")

        return self._features[name]

    def list(self) -> List[str]:
        """
        List all feature names.
        """
        return list(self._features.keys())

    def get_many(self, names: List[str]) -> List[FeatureSpec]:
        """
        Get multiple features by name.
        """
        return [self.get(n) for n in names]

    # ============================================================
    # Discovery (important for agents)
    # ============================================================

    def list_families(self) -> List[str]:
        """
        List unique feature families.
        """
        return sorted(set(f.family for f in self._features.values()))

    def get_by_family(self, family: str) -> List[FeatureSpec]:
        """
        Get all features belonging to a family.
        """
        return [
            f for f in self._features.values()
            if f.family == family
        ]

    def get_by_level(self, level: str) -> List[FeatureSpec]:
        """
        Filter features by level ('asset' or 'systemic').
        """
        return [
            f for f in self._features.values()
            if f.level == level
        ]

    # ============================================================
    # Introspection (agent-ready)
    # ============================================================

    def describe(self) -> List[dict]:
        """
        Return structured metadata for all features.
        """

        return [
            {
                "name": f.name,
                "family": f.family,
                "level": f.level,
                "inputs": f.inputs,
                "n_outputs": len(f.output_columns),
                "frequency": f.frequency,
            }
            for f in self._features.values()
        ]
    def describe_expanded(self) -> List[dict]:
        """
        Return one entry per output column (atomic feature level).
        """

        expanded = []

        for f in self._features.values():

            for col in f.output_columns:
                expanded.append({
                    "name": col,
                    "family": f.family,
                    "level": f.level,
                    "inputs": f.inputs,
                    "source_feature": f.name,  # familia
                    "frequency": f.frequency,
                })

        return expanded

# ============================================================
# Factory (optional but clean)
# ============================================================

def create_registry() -> FeatureRegistry:
    return FeatureRegistry()

