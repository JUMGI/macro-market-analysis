from dataclasses import dataclass, field
from typing import Dict, Any, List
import datetime
from quant_research.research.feature_selection.groups.grouper import FeatureGrouper

@dataclass
class FeatureMetadata:

    dataset_id: str
    dataset_hash: str
    fv_hash: str
    profile: str
    config: Dict[str, Any]
    
    metrics: Dict[str, Dict[str, Any]]
    feature_info: Dict[str, Dict[str, Any]]

    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    version: str = "v1"

    # -------------------------
    # Basic access
    # -------------------------

    def get_feature(self, name: str) -> Dict[str, Any]:
        return self.metrics.get(name, {})
    def get_info(self, name: str) -> Dict[str, Any]:
        return self.feature_info.get(name, {})

    def list_features(self) -> List[str]:
        return list(self.metrics.keys())
    
    # -------------------------
    # 🔥 NUEVO: grouping nativo
    # -------------------------

    def get_feature_groups(self) -> dict:

        grouper = FeatureGrouper()

        return grouper.group(self.feature_info)

    # -------------------------
    # Filtering (MUY IMPORTANTE)
    # -------------------------

    def filter(self, rules: Dict[str, Any]) -> List[str]:
        """
        Returns list of feature names satisfying rules.

        rules example:
        {
            "stability": (">", 0.7),
            "missing": ("<", 0.05)
        }
        """

        selected = []

        for feature, values in self.metrics.items():
            if self._match_rules(values, rules):
                selected.append(feature)

        return selected

    def _match_rules(self, values: Dict[str, Any], rules: Dict[str, Any]) -> bool:

        for key, (op, threshold) in rules.items():

            val = values.get(key)

            if val is None:
                return False

            if op == ">" and not (val > threshold):
                return False
            if op == "<" and not (val < threshold):
                return False
            if op == ">=" and not (val >= threshold):
                return False
            if op == "<=" and not (val <= threshold):
                return False

        return True

    # -------------------------
    # Diagnostics
    # -------------------------

    def summary(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "n_features": len(self.metrics),
            "profile": self.profile,
            "created_at": self.created_at,
            "version": self.version
        }

    # -------------------------
    # Debugging
    # -------------------------

    def top_features(self, metric: str, n: int = 5) -> List[str]:
        """
        Returns top N features by a given metric
        """

        sorted_feats = sorted(
            self.metrics.items(),
            key=lambda x: x[1].get(metric, float("-inf")),
            reverse=True
        )

        return [f[0] for f in sorted_feats[:n]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureMetadata":
        return cls(
            dataset_id=data["dataset_id"],
            dataset_hash=data["dataset_hash"],
            fv_hash=data["fv_hash"],
            profile=data.get("profile", "default"),
            config=data.get("config", {}),
            metrics=data["metrics"],
            created_at=data.get("created_at"),
            version=data.get("version", "v1")
        )