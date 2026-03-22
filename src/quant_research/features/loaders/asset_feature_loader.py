from pathlib import Path
from typing import Optional, List, Dict, Union
import pandas as pd

from quant_research.config.paths import FEATURES_PATH


class FeatureLoader:
    """
    Production-grade Feature Loader aligned with project structure:

    data/features/asset/{family}/{asset}.parquet

    - 1 file per asset
    - index = datetime
    - columns = features
    """

    def __init__(self, base_path: Union[str, Path] = FEATURES_PATH):
        self.base_path = Path(base_path)

        if not self.base_path.exists():
            raise FileNotFoundError(f"Base path not found: {self.base_path}")

    # ============================================================
    # Path resolution
    # ============================================================

    def _get_asset_file(self, family: str, asset: str) -> Path:
        """
        Resolve path:
        data/features/asset/{family}/{asset}.parquet
        """
        path = self.base_path / "asset" / family / f"{asset}.parquet"

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        return path

    # ============================================================
    # Core loader
    # ============================================================

    def load_asset_features(
        self,
        family: str,
        asset: str,
        features: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Load features for a given asset and family.

        Parameters:
        - family: e.g. 'momentum', 'volatility'
        - asset: e.g. 'SPY', 'BTC'
        - features: subset of columns (optional)
        - start/end: date filtering
        """

        path = self._get_asset_file(family, asset)

        df = pd.read_parquet(path)

        # --------------------------------------------
        # Feature filtering
        # --------------------------------------------
        if features is not None:
            missing = [f for f in features if f not in df.columns]
            if missing:
                raise ValueError(f"Missing features: {missing}")

            df = df[features]

        # --------------------------------------------
        # Date filtering
        # --------------------------------------------
        if start or end:
            if not isinstance(df.index, pd.DatetimeIndex):
                raise ValueError("Index must be DatetimeIndex for date filtering")

            if start:
                df = df[df.index >= pd.to_datetime(start)]

            if end:
                df = df[df.index <= pd.to_datetime(end)]

        return df

    # ============================================================
    # Multi-asset loader (clave para panel)
    # ============================================================

    def load_multi_asset(
        self,
        family: str,
        assets: List[str],
        feature: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Load same feature across multiple assets.
        """

        data = {}

        for asset in assets:
            df = self.load_asset_features(
                family=family,
                asset=asset,
                features=[feature] if feature else None,
                start=start,
                end=end,
            )

            data[asset] = df

        return data