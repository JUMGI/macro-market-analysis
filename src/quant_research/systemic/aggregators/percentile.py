import pandas as pd
import numpy as np


def percentile(
    df: pd.DataFrame,
    q: float = 0.5,
) -> pd.Series:
    """
    Cross-sectional percentile.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Percentile expects DataFrame")

    return df.apply(lambda row: np.percentile(row.dropna(), q * 100)
                    if row.notna().sum() > 0 else np.nan, axis=1)