import pandas as pd


def build_feature_panel(asset_data: dict) -> pd.DataFrame:

    """
    Build cross-asset feature panel.

    Parameters
    ----------
    asset_data : dict
        {asset: dataframe}

    Returns
    -------
    DataFrame
        MultiIndex columns (feature, asset)
    """

    dfs = []

    for asset, df in asset_data.items():

        df = df.copy()

        df.columns = pd.MultiIndex.from_product(
            [df.columns, [asset]],
            names=["feature", "asset"]
        )

        dfs.append(df)

    panel = pd.concat(dfs, axis=1)

    panel = panel.sort_index(axis=1)

    return panel
