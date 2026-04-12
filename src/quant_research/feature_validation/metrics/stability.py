import numpy as np
import pandas as pd


def compute_stability(series: pd.Series,full_df=None, window: int = 63) -> float:
    """
    Measures stability of a feature via rolling volatility consistency.

    Returns:
        float in [0, 1] (higher = more stable)
    """

    series = series.dropna()

    if len(series) < window * 2:
        return np.nan

    rolling_std = series.rolling(window).std()

    rolling_std = rolling_std.dropna()

    if rolling_std.mean() == 0:
        return 0.0

    stability = 1 - (rolling_std.std() / rolling_std.mean())

    return float(np.clip(stability, 0, 1))