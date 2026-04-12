import numpy as np
import pandas as pd

"""
def compute_redundancy(series: pd.Series, full_df: pd.DataFrame) -> float:
   
   # Measures max absolute correlation with other features.
    

    if series.name not in full_df.columns:
        return np.nan

    corr_matrix = full_df.corr()

    if series.name not in corr_matrix:
        return np.nan

    correlations = corr_matrix[series.name].drop(series.name)

    if len(correlations) == 0:
        return 0.0

    return float(correlations.abs().max())
"""

def compute_redundancy(
    series,
    full_df=None,
    method: str = "pearson"
):
    """
    Computes redundancy as max correlation with other features.
    """
    VALID_METHODS = {"pearson", "spearman", "kendall"}

    if method not in VALID_METHODS:
        raise ValueError(f"Invalid method: {method}")

    if full_df is None:
        raise ValueError("full_df is required for redundancy metric")

    correlations = full_df.corr(method=method)[series.name].drop(series.name)

    return correlations.abs().max()