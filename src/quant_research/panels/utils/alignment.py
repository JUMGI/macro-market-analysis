import pandas as pd


def align_and_concat(data_dict, method="union"):
    """
    Align and concatenate multiple asset DataFrames into a single panel.

    This function performs cross-asset alignment using pandas' internal
    vectorized operations. It leverages `pd.concat` to efficiently align
    indices and construct a unified DataFrame.

    Parameters
    ----------
    data_dict : dict[str, pd.DataFrame]
        Dictionary mapping asset identifiers to DataFrames.
        Each DataFrame must:
            - have a DatetimeIndex
            - contain feature columns
    method : str, default "union"
        Alignment strategy across assets:
            - "union": outer join, includes all timestamps
            - "intersection": inner join, keeps only common timestamps

    Returns
    -------
    pd.DataFrame
        Combined panel with:
            - index: datetime (aligned across assets)
            - columns: MultiIndex (asset, feature)

    Notes
    -----
    - This operation is fully vectorized and relies on pandas internals.
    - "union" will introduce NaNs where assets have missing history.
    - "intersection" reduces NaNs but may significantly shorten the time span.
    """

    if method not in ["union", "intersection"]:
        raise ValueError(f"Unknown alignment method: {method}")

    # Determine join type based on alignment strategy
    join_type = "outer" if method == "union" else "inner"

    # Concatenate across assets, producing MultiIndex columns (asset, feature)
    panel = pd.concat(
        data_dict,
        axis=1,
        join=join_type
    )

    return panel