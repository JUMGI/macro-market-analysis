import pandas as pd


def compute_missing(series: pd.Series, full_df=None) -> float:
    """
    Fraction of missing values.
    """

    if len(series) == 0:
        return 1.0

    return float(series.isna().mean())