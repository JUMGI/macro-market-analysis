from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class FeatureSpec:
    name: str
    family: str
    asset_level: str
    column: str
    
    inputs: List[str]
    parameters: Dict
    
    compute_fn: Callable
    frequency: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Feature must have a name")
        
        if self.column != self.name:
            raise ValueError("column must match name (convention)")