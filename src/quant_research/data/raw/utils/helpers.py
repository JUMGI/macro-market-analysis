# ============================================================
# RAW DATA HELPERS
# ============================================================

from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

from quant_research.config.paths import RAW_DATA_PATH
from quant_research.data.registry.universe_registry import Asset
from quant_research.data.raw.utils.io import load_parquet


# ============================================================
# Constants
# ============================================================

EXPECTED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
    "Dividends",
    "Stock Splits",
    "Capital Gains",
]





# ============================================================
# Metadata helpers
# ============================================================

def get_last_date(asset) -> pd.Timestamp:
    path = RAW_DATA_PATH / f"{asset.symbol}.parquet"

    if not path.exists():
        return None

    df = pd.read_parquet(path)

    ts = df.index.max()

    # 🔥 critical fix
    if ts.tzinfo is not None:
        ts = ts.tz_convert(None)

    return ts




# ============================================================
# Validation
# ============================================================

def validate_download(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic sanity checks:
    - datetime index
    - sorted index
    - no duplicated timestamps
    """

    if df.empty:
        return df

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]

    return df


# ============================================================
# Normalization
# ============================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce consistent raw data schema.
    """

    if df.empty:
        return df

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0

    return df[EXPECTED_COLUMNS]


# ============================================================
# Merge
# ============================================================

def merge_with_existing(df_new: pd.DataFrame, asset: Asset) -> pd.DataFrame:
    """
    Merge new data with existing stored dataset.
    """

    df_old = load_parquet(asset)

    if df_old is None:
        return df_new

    # flatten columns if needed
    if isinstance(df_old.columns, pd.MultiIndex):
        df_old.columns = df_old.columns.get_level_values(0)

    if isinstance(df_new.columns, pd.MultiIndex):
        df_new.columns = df_new.columns.get_level_values(0)

    df = pd.concat([df_old, df_new])
    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()

    return df

def adjust_end_date_for_yfinance(end_date: pd.Timestamp) -> pd.Timestamp:
    """
    yfinance uses exclusive end date.

    We shift by +1 day to make it inclusive.
    """
    return end_date + pd.Timedelta(days=1)

