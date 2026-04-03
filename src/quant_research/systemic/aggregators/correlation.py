import pandas as pd
import numpy as np


def correlation(
    df: pd.DataFrame,
    window: int = 20,
) -> pd.Series:

    # ------------------------------------------------
    # 1. rolling correlation
    # ------------------------------------------------
    rolling_corr = df.rolling(window).corr()

    # ------------------------------------------------
    # 2. función EXACTA del notebook
    # ------------------------------------------------
    def mean_correlation(corr_matrix: pd.DataFrame):

        # si no hay matriz válida
        if not isinstance(corr_matrix, pd.DataFrame):
            return np.nan

        if corr_matrix.shape[0] < 2:
            return np.nan

        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

        values = corr_matrix.where(mask).stack()

        if values.empty:
            return np.nan

        return values.mean()

    # ------------------------------------------------
    # 3. AGRUPAR POR FECHA (igual que notebook)
    # ------------------------------------------------
    result = rolling_corr.groupby(level=0).apply(mean_correlation)

    return result