import pandas as pd


def zscore(
    data,
    window: int = 20,
    min_periods: int | None = None,
):
    """
    Rolling z-score.

    Works with Series (preferred) or DataFrame.
    """

    if min_periods is None:
        min_periods = window

    rolling_mean = data.rolling(window, min_periods=min_periods).mean()
    rolling_std = data.rolling(window, min_periods=min_periods).std()

    return (data - rolling_mean) / rolling_std