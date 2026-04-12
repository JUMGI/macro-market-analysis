import numpy as np
import pandas as pd


def compute_autocorr(series: pd.Series, full_df=None, lag: int = 1) -> float:
    """
    Computes autocorrelation at given lag.
    """

    series = series.dropna()

    if len(series) < lag + 10:
        return np.nan

    return float(series.autocorr(lag=lag))