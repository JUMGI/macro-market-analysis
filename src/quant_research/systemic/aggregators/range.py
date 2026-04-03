import pandas as pd
import numpy as np


def range_(
    df: pd.DataFrame,
    min_count: int = 1,
) -> pd.Series:
    """
    Cross-sectional range (max - min).
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Range expects DataFrame")

    def _range(row):
        x = row.dropna().values
        if len(x) < min_count:
            return np.nan
        return np.max(x) - np.min(x)

    return df.apply(_range, axis=1)