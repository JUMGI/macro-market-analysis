from typing import Optional
import pandas as pd

from quant_research.data.registry.universe_registry import Asset


def adjust_end_date_for_yfinance(end_date: pd.Timestamp) -> pd.Timestamp:
    """
    yfinance uses exclusive end date.
    We shift by +1 day to make it inclusive.
    """
    return end_date + pd.Timedelta(days=1)


def get_effective_today(asset: Asset, end: Optional[str] = None) -> pd.Timestamp:
    """
    Determine last safe date for an asset without lookahead bias.
    """

    if end is not None:
        return pd.to_datetime(end)

    now = pd.Timestamp.utcnow().tz_localize(None)
    today = now.normalize()

    if asset.asset_type == "crypto":
        # Crypto candle closes at 00:00 UTC next day
        if now.hour < 1:
            return today - pd.Timedelta(days=2)
        else:
            return today - pd.Timedelta(days=1)

    else:
        # Equities / ETFs / bonds
        return today - pd.Timedelta(days=1)