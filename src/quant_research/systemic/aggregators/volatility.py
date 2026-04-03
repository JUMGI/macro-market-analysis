import pandas as pd


def volatility(
    df: pd.DataFrame,
    method: str = "std",
    skipna: bool = True,
) -> pd.Series:
    """
    Cross-sectional volatility proxy.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Volatility expects DataFrame")

    if method == "std":
        return df.std(axis=1, skipna=skipna)

    elif method == "var":
        return df.var(axis=1, skipna=skipna)

    else:
        raise ValueError(f"Unknown method: {method}")