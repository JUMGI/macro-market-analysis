from pathlib import Path
from typing import Dict, List

import pandas as pd

from quant_research.config.paths import RAW_DATA_PATH
from quant_research.data.registry.universe_registry import Asset


class AssetRawDataLoader:
    """
    Load raw market data from storage.

    Responsibilities:
    - read parquet
    - enforce minimal structural integrity

    Does NOT:
    - transform data
    - apply business logic
    """

    def __init__(self, base_path: Path = RAW_DATA_PATH):
        self.base_path = Path(base_path)

    # --------------------------------------------------------
    # SINGLE ASSET
    # --------------------------------------------------------
    def load_asset(self, asset: Asset) -> pd.DataFrame:

        path = self.base_path / f"{asset.symbol}.parquet"

        if not path.exists():
            raise FileNotFoundError(f"Raw data not found: {path}")

        df = pd.read_parquet(path)

        # ----------------------------------------
        # Minimal integrity enforcement
        # ----------------------------------------

        # datetime index
        df.index = pd.to_datetime(df.index)

        # sort
        df = df.sort_index()

        # remove duplicates
        df = df[~df.index.duplicated(keep="last")]

        return df

    # --------------------------------------------------------
    # MULTI ASSET
    # --------------------------------------------------------
    def load_universe(self, assets: List[Asset]) -> Dict[str, pd.DataFrame]:

        data = {}

        for asset in assets:
            df = self.load_asset(asset)
            data[asset.symbol] = df

        return data