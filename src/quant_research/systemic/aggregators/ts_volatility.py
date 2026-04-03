import pandas as pd


def ts_volatility(
    df: pd.DataFrame,
    method: str = "mean",
    window: int = 20,
    min_periods: int | None = None,
) -> pd.Series:
    """
    Time-series volatility of a systemic signal.

    Steps:
    1. Aggregate cross-section (mean/median)
    2. Compute rolling volatility

    Parameters
    ----------
    df : DataFrame (date x assets)

    method : str
        "mean" | "median"

    window : int
        Rolling window

    Returns
    -------
    pd.Series
    """

    if min_periods is None:
        min_periods = window

    # ----------------------------------------
    # 1. Cross-sectional aggregation
    # ----------------------------------------
    if method == "mean":
        series = df.mean(axis=1)

    elif method == "median":
        series = df.median(axis=1)

    else:
        raise ValueError(f"Unknown method: {method}")

    # ----------------------------------------
    # 2. Rolling volatility
    # ----------------------------------------
    return series.rolling(window, min_periods=min_periods).std()