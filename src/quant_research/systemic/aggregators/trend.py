import pandas as pd
import numpy as np


def trend(
    df: pd.DataFrame,
    method: str = "mean",
    skipna: bool = True,
    min_count: int = 1,
    trim_pct: float = 0.1,
    winsor_pct: float = 0.1,
    threshold: float = 0.0,
    weights: dict | None = None,
) -> pd.Series:
    """
    Flexible cross-asset trend aggregator.

    Parameters
    ----------
    df : pd.DataFrame
        index = date, columns = assets

    method : str
        "mean" | "median" | "trimmed" | "winsorized" | "breadth" | "weighted"

    trim_pct : float
        % to trim from each tail (for trimmed mean)

    winsor_pct : float
        % to cap at tails (for winsorization)

    threshold : float
        Used for breadth (e.g. > 0)

    weights : dict
        {column_name: weight}

    Returns
    -------
    pd.Series
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Trend expects a DataFrame")

    # ------------------------------------------------
    # MEAN
    # ------------------------------------------------
    if method == "mean":
        return df.mean(axis=1, skipna=skipna, min_count=min_count)

    # ------------------------------------------------
    # MEDIAN
    # ------------------------------------------------
    elif method == "median":
        return df.median(axis=1, skipna=skipna)

    # ------------------------------------------------
    # TRIMMED MEAN
    # ------------------------------------------------
    elif method == "trimmed":

        def _trim(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan

            x = np.sort(x)
            k = int(len(x) * trim_pct)

            if len(x) - 2 * k <= 0:
                return np.nan

            return x[k:-k].mean()

        return df.apply(_trim, axis=1)

    # ------------------------------------------------
    # WINSORIZED MEAN
    # ------------------------------------------------
    elif method == "winsorized":

        def _winsor(row):
            x = row.dropna().values
            if len(x) < min_count:
                return np.nan

            lower = np.percentile(x, winsor_pct * 100)
            upper = np.percentile(x, (1 - winsor_pct) * 100)

            x = np.clip(x, lower, upper)

            return x.mean()

        return df.apply(_winsor, axis=1)

    # ------------------------------------------------
    # BREADTH
    # ------------------------------------------------
    elif method == "breadth":
        valid = df.notna().sum(axis=1)
        positive = (df > threshold).sum(axis=1)
        return positive / valid

    # ------------------------------------------------
    # WEIGHTED MEAN
    # ------------------------------------------------
    elif method == "weighted":

        if weights is None:
            raise ValueError("Weights required for weighted trend")

        w = pd.Series(weights)

        # alinear weights con columnas
        w = w.reindex(df.columns).fillna(0)

        weighted_sum = (df * w).sum(axis=1)
        weight_sum = w.sum()

        return weighted_sum / weight_sum

    else:
        raise ValueError(f"Unknown trend method: {method}")