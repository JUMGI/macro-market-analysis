import pandas as pd


def skew(
    df: pd.DataFrame,
    skipna: bool = True,
) -> pd.Series:
    """
    Cross-sectional skewness.

    Measures asymmetry across assets.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Skew expects DataFrame")

    return df.skew(axis=1, skipna=skipna)