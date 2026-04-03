import pandas as pd
import numpy as np


def breadth(
    df: pd.DataFrame,
    method: str = "standard",
    threshold: float = 0.0,
    weights: dict | None = None,
    q: float = 0.7,
) -> pd.Series:
    """
    Cross-asset breadth aggregator.

    Parameters
    ----------
    df : pd.DataFrame
        index = date, columns = assets

    method : str
        "standard" | "symmetric" | "weighted" | "percentile"

    threshold : float
        Used for standard/symmetric (e.g. 0 for momentum)

    weights : dict
        Used for weighted breadth

    q : float
        Percentile threshold (for percentile method)

    Returns
    -------
    pd.Series
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Breadth expects a DataFrame")

    # ------------------------------------------------
    # STANDARD BREADTH
    # ------------------------------------------------
    if method == "standard":
        valid = df.notna().sum(axis=1)
        positive = (df > threshold).sum(axis=1)
        return positive / valid

    # ------------------------------------------------
    # SYMMETRIC BREADTH
    # ------------------------------------------------
    elif method == "symmetric":
        valid = df.notna().sum(axis=1)

        positive = (df > threshold).sum(axis=1)
        negative = (df < -threshold).sum(axis=1)

        return (positive - negative) / valid

    # ------------------------------------------------
    # WEIGHTED BREADTH
    # ------------------------------------------------
    elif method == "weighted":

        if weights is None:
            raise ValueError("Weights required for weighted breadth")

        w = pd.Series(weights).reindex(df.columns).fillna(0)

        signal = (df > threshold).astype(float)

        weighted = (signal * w).sum(axis=1)
        total_w = w.sum()

        return weighted / total_w

    # ------------------------------------------------
    # PERCENTILE BREADTH
    # ------------------------------------------------
    elif method == "percentile":

        def _pct(row):
            x = row.dropna().values
            if len(x) == 0:
                return np.nan

            cutoff = np.percentile(x, q * 100)
            return np.mean(x > cutoff)

        return df.apply(_pct, axis=1)

    else:
        raise ValueError(f"Unknown breadth method: {method}")