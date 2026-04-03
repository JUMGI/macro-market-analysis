import pandas as pd
import numpy as np


def dispersion(
    df: pd.DataFrame,
    method: str = "std",
    skipna: bool = True,
    min_count: int = 1,
    q_low: float = 0.1,
    q_high: float = 0.9,
) -> pd.Series:
    """
    Cross-sectional dispersion of assets.

    Parameters
    ----------
    df : pd.DataFrame
        index = date, columns = assets

    method : str
        "std" | "mad" | "range" | "iqr" | "percentile" | "var"

    q_low : float
        Lower quantile (for percentile method)

    q_high : float
        Upper quantile

    Returns
    -------
    pd.Series
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Dispersion expects a DataFrame")

    # ------------------------------------------------
    # STD
    # ------------------------------------------------
    if method == "std":
        return df.std(axis=1, skipna=skipna)

    # ------------------------------------------------
    # VARIANCE
    # ------------------------------------------------
    elif method == "var":
        return df.var(axis=1, skipna=skipna)

    # ------------------------------------------------
    # MAD (median absolute deviation)
    # ------------------------------------------------
    elif method == "mad":

        def _mad(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan
            med = np.median(x)
            return np.median(np.abs(x - med))

        return df.apply(_mad, axis=1)

    # ------------------------------------------------
    # RANGE
    # ------------------------------------------------
    elif method == "range":

        def _range(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan
            return np.max(x) - np.min(x)

        return df.apply(_range, axis=1)

    # ------------------------------------------------
    # IQR (Q75 - Q25)
    # ------------------------------------------------
    elif method == "iqr":

        def _iqr(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan
            return np.percentile(x, 75) - np.percentile(x, 25)

        return df.apply(_iqr, axis=1)

    # ------------------------------------------------
    # PERCENTILE SPREAD
    # ------------------------------------------------
    elif method == "percentile":

        def _pct(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan
            return np.percentile(x, q_high * 100) - np.percentile(x, q_low * 100)

        return df.apply(_pct, axis=1)

    else:
        raise ValueError(f"Unknown dispersion method: {method}")