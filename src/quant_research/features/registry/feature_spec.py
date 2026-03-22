from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class FeatureSpec:
    """
    Feature specification (family-level, agent-ready).

    Represents a feature generation engine and its metadata.
    """

    name: str                  # e.g. "momentum"
    family: str                # same as name (for now)
    level: str                 # "asset" | "systemic"

    inputs: List[str]          # required columns in raw data
    parameters: Dict           # config parameters (optional)

    compute_fn: Callable       # compute_fn(df_raw) -> df_features

    output_columns: List[str]  # ALL columns produced by compute_fn

    frequency: str             # e.g. "daily"

    # ============================================================
    # Validation
    # ============================================================

    def __post_init__(self):
        if not self.name:
            raise ValueError("Feature must have a name")

        if not callable(self.compute_fn):
            raise ValueError("compute_fn must be callable")

        if not self.output_columns:
            raise ValueError("output_columns must be defined")

        if self.level not in {"asset", "systemic"}:
            raise ValueError("level must be 'asset' or 'systemic'")