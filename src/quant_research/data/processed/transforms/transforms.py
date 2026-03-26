# ============================================================
# TRANSFORMS - PROCESSED DATA LAYER
# ============================================================

import numpy as np
import pandas as pd


# ============================================================
# RAW NORMALIZATION
# ============================================================

def normalize_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize raw vendor data:
    - rename columns
    - ensure datetime index
    - sort chronologically
    """

    # rename vendor column
    if "Adj Close" in df.columns:
        df = df.rename(columns={"Adj Close": "vendor_adj_close"})

    # ensure datetime index
    df.index = pd.to_datetime(df.index)

    # sort index
    df = df.sort_index()

    return df


def ensure_corporate_action_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure corporate action columns exist.
    Missing columns are filled with 0.0.
    """

    for col in ["Dividends", "Stock Splits", "Capital Gains"]:
        if col not in df.columns:
            df[col] = 0.0

    return df


def remove_duplicate_index(df: pd.DataFrame, asset: str = "") -> pd.DataFrame:
    """
    Remove duplicated timestamps (keep first occurrence).
    """

    if df.index.duplicated().any():
        n_dup = df.index.duplicated().sum()
        print(f"⚠ {asset} has {n_dup} duplicated timestamps")

        df = df[~df.index.duplicated(keep="first")]

        print(f"{asset} duplicates removed")

    return df


# ============================================================
# CORPORATE ACTIONS → TOTAL RETURN SERIES
# ============================================================

def compute_distribution(df: pd.DataFrame, include_capital_gains: bool = True) -> pd.DataFrame:
    """
    Compute total distribution (dividends + capital gains).
    """

    dist = df["Dividends"].fillna(0.0)

    if include_capital_gains and "Capital Gains" in df.columns:
        dist = dist + df["Capital Gains"].fillna(0.0)

    df["distribution"] = dist

    return df


def compute_dist_factor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute distribution adjustment factor.
    """

    prev_close = df["Close"].shift(1)

    df["dist_factor"] = 1 - (df["distribution"] / prev_close)

    # handle numerical issues
    df["dist_factor"] = df["dist_factor"].replace([np.inf, -np.inf], np.nan)

    # default factor = 1 (no distribution)
    df["dist_factor"] = df["dist_factor"].fillna(1.0)

    return df


def compute_cum_adj_factor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cumulative adjustment factor (backward).
    """

    factors = df["dist_factor"].fillna(1.0)

    df["cum_adj_factor"] = factors[::-1].cumprod()[::-1]

    return df


def compute_adj_close(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute total return adjusted close price.
    """

    df["adj_close"] = df["Close"] * df["cum_adj_factor"]

    return df


def compute_total_return_series(
    df: pd.DataFrame,
    include_capital_gains: bool = True
) -> pd.DataFrame:
    """
    Full pipeline to construct total return price series.
    """

    df = compute_distribution(df, include_capital_gains)
    df = compute_dist_factor(df)
    df = compute_cum_adj_factor(df)
    df = compute_adj_close(df)

    return df


# ============================================================
# RETURNS
# ============================================================

def compute_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily log returns.
    """

    log_price = np.log(df["adj_close"])

    df["log_ret"] = log_price.diff(1)

    return df


def compute_multi_horizon_returns(
    df: pd.DataFrame,
    windows: list[int]
) -> pd.DataFrame:
    """
    Compute multi-horizon log returns.
    """

    log_price = np.log(df["adj_close"])

    for h in windows:
        df[f"log_ret_{h}"] = log_price.diff(h)

    return df


def compute_return_features(
    df: pd.DataFrame,
    windows: list[int]
) -> pd.DataFrame:
    """
    Full return feature pipeline.
    """

    df = compute_log_returns(df)
    df = compute_multi_horizon_returns(df, windows)

    return df


# ============================================================
# LIQUIDITY FEATURES
# ============================================================

def compute_dollar_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute dollar volume (liquidity proxy).
    """

    df["dollar_volume"] = df["Close"] * df["Volume"]

    return df


def compute_rolling_liquidity(
    df: pd.DataFrame,
    windows: list[int]
) -> pd.DataFrame:
    """
    Compute rolling liquidity metrics.
    """

    for w in windows:
        df[f"dollar_volume_{w}"] = df["dollar_volume"].rolling(w).mean()

    return df


def compute_liquidity_features(
    df: pd.DataFrame,
    windows: list[int]
) -> pd.DataFrame:
    """
    Full liquidity feature pipeline.
    """

    df = compute_dollar_volume(df)
    df = compute_rolling_liquidity(df, windows)

    return df


# ============================================================
# UTILITIES
# ============================================================

def clean_columns_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unwanted column metadata (e.g., inherited names from vendor).
    """

    df.columns.name = None

    return df

def enforce_column_order(df, columns):
    """
    Ensure consistent column order and presence.
    """

    # add missing columns if needed
    for col in columns:
        if col not in df.columns:
            df[col] = np.nan

    # reorder
    df = df[columns]

    return df
# ============================================================
# FULL PIPELINE (END-TO-END)
# ============================================================

def process_asset_pipeline(
    df: pd.DataFrame,
    return_windows: list[int],
    liquidity_windows: list[int],
    include_capital_gains: bool = True,
    asset: str = ""
) -> pd.DataFrame:
    """
    End-to-end processing pipeline for a single asset.
    """

    # --- raw normalization ---
    df = normalize_raw_data(df)
    df = ensure_corporate_action_columns(df)
    df = remove_duplicate_index(df, asset)

    # --- corporate actions ---
    df = compute_total_return_series(df, include_capital_gains)

    # --- returns ---
    df = compute_return_features(df, return_windows)

    # --- liquidity ---
    df = compute_liquidity_features(df, liquidity_windows)

    # --- cleanup ---
    df = clean_columns_metadata(df)

    return df

