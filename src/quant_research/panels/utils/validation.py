def validate_assets(merged_assets):
    """
    Validate structural consistency of asset-level feature DataFrames.

    This function ensures that all asset DataFrames are compatible
    for cross-asset panel construction.

    Parameters
    ----------
    merged_assets : dict[str, pd.DataFrame]
        Dictionary mapping asset identifiers to DataFrames.
        Each DataFrame should represent merged feature families for an asset.

    Raises
    ------
    ValueError
        If any of the following conditions are violated:
            - index is not sorted (monotonic increasing)
            - duplicated timestamps are present
            - feature columns differ across assets

    Notes
    -----
    These validations are critical to ensure:
        - correct temporal alignment
        - consistent feature space across assets
        - reliability of downstream models and analysis
    """

    columns_ref = None

    for asset, df in merged_assets.items():

        # Ensure time index is sorted
        if not df.index.is_monotonic_increasing:
            raise ValueError(f"{asset}: index not sorted")

        # Ensure no duplicated timestamps
        if df.index.duplicated().any():
            raise ValueError(f"{asset}: duplicated timestamps")

        # Ensure consistent feature set across assets
        if columns_ref is None:
            columns_ref = df.columns
        else:
            if not df.columns.equals(columns_ref):
                raise ValueError(f"{asset}: columns mismatch")