from pathlib import Path
from typing import Optional

import pandas as pd

from quant_research.config.paths import RAW_DATA_PATH
from quant_research.data.registry.universe_registry import Asset


def _get_path(asset: Asset) -> Path:
    return RAW_DATA_PATH / f"{asset.symbol}.parquet"


def parquet_exists(asset: Asset) -> bool:
    return _get_path(asset).exists()


def load_parquet(asset: Asset) -> Optional[pd.DataFrame]:
    path = _get_path(asset)
    if not path.exists():
        return None
    return pd.read_parquet(path)


def save_parquet(df: pd.DataFrame, asset: Asset) -> None:
    path = _get_path(asset)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.to_parquet(path, engine="pyarrow")