# research/core/search_space/schema.py

from typing import Dict, List, Any, TypedDict


class FeatureSelection(TypedDict):
    type: str  # "top_k" | "all"
    k: int | None


class FeatureGroupSpace(TypedDict):
    candidates: List[str]
    selection: FeatureSelection


FeatureSpace = Dict[str, FeatureGroupSpace]


class ParamConfig(TypedDict):
    type: str  # "grid" | "fixed"
    values: List[Any]


ParameterSpace = Dict[str, ParamConfig]


class SearchSpace(TypedDict):
    features: FeatureSpace
    params: ParameterSpace


class Sample(TypedDict):
    features: Dict[str, str]
    params: Dict[str, Any]