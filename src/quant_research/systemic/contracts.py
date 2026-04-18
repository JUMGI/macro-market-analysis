from dataclasses import dataclass
from typing import Dict, Any
import pandas as pd


@dataclass(frozen=True)
class SystemicMetadata:
    name: str
    dataset_hash: str
    config_hash: str
    n_rows: int
    n_features: int

    # 🔥 clave: metadata rica
    features: Dict[str, Dict[str, Any]]


@dataclass(frozen=True)
class SystemicDatasetBundle:
    data: pd.DataFrame
    data_z: pd.DataFrame
    metadata: SystemicMetadata