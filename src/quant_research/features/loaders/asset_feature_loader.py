from pathlib import Path
from typing import Optional, List, Dict, Union
import pandas as pd

from quant_research.config.paths import FEATURES_PATH


class FeatureLoader:
    """
    Production-grade Feature Loader aligned with project structure:

    data/features/asset/{family}/{asset}.parquet

    Conventions:
    - 1 file per asset
    - index = DatetimeIndex (sorted, unique)
    - columns = features
    """

    # ============================================================
    # INIT
    # ============================================================

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

        family_path = self.base_path / "asset" / family

        if not family_path.exists():
            raise ValueError(f"Unknown feature family: {family}")

        path = family_path / f"{asset}.parquet"

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

        Parameters
        ----------
        family : str
            Feature family (e.g. 'momentum', 'volatility')
        asset : str
            Asset symbol (e.g. 'SPY', 'BTC')
        features : list[str], optional
            Subset of features to load
        start : str, optional
            Start date (inclusive)
        end : str, optional
            End date (inclusive)

        Returns
        -------
        pd.DataFrame
            Feature dataframe with DatetimeIndex and feature columns
        """

        path = self._get_asset_file(family, asset)

        # --------------------------------------------------------
        # Load & enforce ordering
        # --------------------------------------------------------
        df = pd.read_parquet(path).sort_index()

        # --------------------------------------------------------
        # Index validation (CRITICAL)
        # --------------------------------------------------------
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError(f"{asset} ({family}): Index must be DatetimeIndex")

        if not df.index.is_monotonic_increasing:
            raise ValueError(f"{asset} ({family}): Index must be sorted")

        if df.index.has_duplicates:
            raise ValueError(f"{asset} ({family}): Index contains duplicates")

        if df.empty:
            raise ValueError(f"{asset} ({family}): Feature file is empty")

        # --------------------------------------------------------
        # Feature filtering
        # --------------------------------------------------------
        if features is not None:
            missing = [f for f in features if f not in df.columns]

            if missing:
                raise ValueError(
                    f"{asset} ({family}): Missing features: {missing}"
                )

            df = df[features]

        # --------------------------------------------------------
        # Date filtering
        # --------------------------------------------------------
        if start or end:
            if start:
                start_dt = pd.to_datetime(start)
                df = df[df.index >= start_dt]

            if end:
                end_dt = pd.to_datetime(end)
                df = df[df.index <= end_dt]

        return df

    # ============================================================
    # Multi-asset loader (panel-ready)
    # ============================================================

    def load_assets_features(
        self,
        family: str,
        assets: List[str],
        features: Optional[List[str]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Load features for multiple assets within a family.

        Parameters
        ----------
        family : str
            Feature family
        assets : list[str]
            List of asset symbols
        features : list[str], optional
            Subset of features
        start : str, optional
            Start date
        end : str, optional
            End date

        Returns
        -------
        dict[str, pd.DataFrame]
            Mapping: asset -> feature DataFrame
        """

        data = {}

        for asset in assets:
            df = self.load_asset_features(
                family=family,
                asset=asset,
                features=features,
                start=start,
                end=end,
            )

            data[asset] = df

        return data