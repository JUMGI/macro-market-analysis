import pandas as pd
import numpy as np


def mean(
    df: pd.DataFrame,
    skipna: bool = True,
    min_count: int = 1,
) -> pd.Series:
    """
    Cross-sectional mean with explicit min_count handling.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Mean aggregator expects a DataFrame input")

    # mean estándar
    mean_vals = df.mean(axis=1, skipna=skipna)

    # conteo de datos válidos
    valid_count = df.notna().sum(axis=1)

    # aplicar min_count manualmente
    mean_vals[valid_count < min_count] = np.nan

    return mean_vals