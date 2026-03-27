from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from quant_research.config.paths import PROCESSED_DATA_PATH


class AssetProcessedDataLoader:
    """
    Load processed market data from storage.

    This is the main entry point for:
    - feature pipelines
    - validators
    - research notebooks
    """

    def __init__(self, base_path: Path = PROCESSED_DATA_PATH):
        self.base_path = Path(base_path)

    # --------------------------------------------------------
    # SINGLE ASSET
    # --------------------------------------------------------
    def load_asset(
        self,
        asset: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:

        path = self.base_path / f"{asset}.parquet"

        if not path.exists():
            raise FileNotFoundError(f"Processed data not found: {path}")

        df = pd.read_parquet(path)

        # ----------------------------------------
        # Optional time filtering
        # ----------------------------------------

        if start:
            df = df[df.index >= pd.to_datetime(start)]

        if end:
            df = df[df.index <= pd.to_datetime(end)]

        return df

    # --------------------------------------------------------
    # MULTI ASSET
    # --------------------------------------------------------
    def load_universe(
        self,
        assets: List[str],
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:

        data = {}

        for asset in assets:
            data[asset] = self.load_asset(asset, start, end)

        return data