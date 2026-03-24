# ============================================================
# RAW DATA HELPER FUNCTIONS
# ============================================================

from quant_research.config.paths import RAW_DATA_PATH
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# ------------------------------------------------------------
# Expected schema
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Helper: check if parquet exists for an asset
# ------------------------------------------------------------
def parquet_exists(asset_symbol: str) -> bool:
    file_path = RAW_DATA_PATH / f"{asset_symbol}.parquet"
    return file_path.exists()

# ------------------------------------------------------------
# Helper: get last date in existing parquet
# ------------------------------------------------------------
def get_last_date(asset_symbol: str) -> pd.Timestamp:
    file_path = RAW_DATA_PATH / f"{asset_symbol}.parquet"
    if file_path.exists():
        df = pd.read_parquet(file_path)
        return df.index.max()
    else:
        return None

# ------------------------------------------------------------
# Helper: download yfinance data for an asset
# ------------------------------------------------------------
def download_asset(asset, start_date=None, end_date=None, interval="1d",
                   auto_adjust=False, actions=True):

    ticker = asset.get_ticker()

    df = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=auto_adjust,
        actions=actions,
        progress=False
    )

    if df.empty:
        print(f"Warning: no data for {ticker}")
        return df

    # flatten yfinance columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index = pd.to_datetime(df.index)

    return df

# ============================================================
# VALIDATE DOWNLOADED DATA
# ============================================================

def validate_download(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic sanity checks on downloaded market data.

    Raw data should remain as close as possible to the source.
    No rows are removed except duplicated timestamps.
    """

    if df.empty:
        return df

    # ensure datetime index
    df.index = pd.to_datetime(df.index)

    # sort by date
    df = df.sort_index()

    # remove duplicated timestamps (can happen in incremental downloads)
    df = df[~df.index.duplicated(keep="last")]

    return df

# ============================================================
# NORMALIZE RAW DATA COLUMNS
# ============================================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure all raw market datasets share the same schema.

    Some assets (especially ETFs) include additional columns
    such as 'Capital Gains'. Others may omit them.

    This function guarantees a consistent column structure.
    """

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0

    # enforce column order
    df = df[EXPECTED_COLUMNS]

    return df

# ============================================================
# MERGE WITH EXISTING DATA
# ============================================================

def merge_with_existing(df_new: pd.DataFrame, symbol: str) -> pd.DataFrame:

    path = RAW_DATA_PATH / f"{symbol}.parquet"

    if not path.exists():
        return df_new

    df_old = pd.read_parquet(path)

    # --------------------------------------------------------
    # Flatten columns if needed
    # --------------------------------------------------------

    if isinstance(df_old.columns, pd.MultiIndex):
        df_old.columns = df_old.columns.get_level_values(0)

    if isinstance(df_new.columns, pd.MultiIndex):
        df_new.columns = df_new.columns.get_level_values(0)

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    df = pd.concat([df_old, df_new])

    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()

    return df
# ------------------------------------------------------------
# Helper: save to parquet
# ------------------------------------------------------------
def save_parquet(df: pd.DataFrame, asset_symbol: str):
    """
    Save dataframe to parquet file.
    """
    file_path = RAW_DATA_PATH / f"{asset_symbol}.parquet"

    df.to_parquet(file_path, engine="pyarrow")




