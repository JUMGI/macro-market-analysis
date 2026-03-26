from quant_research.config.paths import RAW_DATA_PATH
from quant_research.data.processed.io.io import load_raw_parquet
from quant_research.data.processed.transforms.transforms import (
    normalize_raw_data,
    ensure_corporate_action_columns,
    remove_duplicate_index
)
from quant_research.data.processed.validators.validators import validate_expected_columns


def load_asset_data(asset):

    symbol = asset.symbol
    path = RAW_DATA_PATH / f"{symbol}.parquet"

    print(f"\nLoading {symbol} from {path}")

    df = load_raw_parquet(path)

    # --- normalization ---
    df = normalize_raw_data(df)

    # --- validation ---
    validate_expected_columns(df, symbol)

    # --- repair / completion ---
    df = ensure_corporate_action_columns(df)

    # --- integrity ---
    df = remove_duplicate_index(df, symbol)

    return df


def load_raw_dataset(assets):

    data = {}

    for asset in assets:
        symbol = asset.symbol
        df = load_asset_data(asset)
        data[symbol] = df

    print("\nAssets loaded:")
    print(list(data.keys()))

    return data