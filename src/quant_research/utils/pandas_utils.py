# ============================================================
# pandas_utils.py
# ============================================================

import pandas as pd


def flatten_multiindex_series(s: pd.Series) -> pd.DataFrame:
    """
    Convert a MultiIndex pandas Series into a flat DataFrame.

    Expected input:
        index: MultiIndex (e.g. asset, feature)
        values: numeric

    Output:
        DataFrame with columns: [asset, feature, value]
    """
    df = s.reset_index()
    df.columns = ["asset", "feature", "value"]
    return df