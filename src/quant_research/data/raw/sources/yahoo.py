# ============================================================
# YAHOO DATA SOURCE
# ============================================================

from typing import Optional
import pandas as pd
import yfinance as yf

from quant_research.data.registry.universe_registry import Asset


def download_ohlcv(
    asset: Asset,
    start_date: Optional[str],
    end_date: Optional[str],
    interval: str = "1d",
    auto_adjust: bool = False,
    actions: bool = True,
) -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance.
    """

    ticker = asset.get_ticker()

    df = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=auto_adjust,
        actions=actions,
        progress=False,
    )

    if df.empty:
        return df

    # flatten multiindex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index = pd.to_datetime(df.index)

    return df