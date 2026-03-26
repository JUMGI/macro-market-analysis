# ============================================================
# PROCESSOR - PROCESSED DATA PIPELINE
# ============================================================

from quant_research.config.paths import RAW_DATA_PATH, PROCESSED_DATA_PATH

from quant_research.data.registry.universe_registry import get_all_assets

from quant_research.data.processed.loaders.loaders import load_raw_dataset

from quant_research.data.processed.transforms.transforms import process_asset_pipeline

from quant_research.data.processed.io.io import save_processed_dataset

from quant_research.data.processed.config.config import (
    RETURN_WINDOWS,
    LIQUIDITY_WINDOWS,
    PROCESSED_COLUMNS
)


# ============================================================
# PROCESS SINGLE ASSET
# ============================================================

def process_asset(asset, raw_data: dict):

    symbol = asset.symbol

    print(f"\nProcessing asset: {symbol}")

    df_raw = raw_data[symbol]

    df_processed = process_asset_pipeline(
        df_raw.copy(),
        return_windows=RETURN_WINDOWS,
        liquidity_windows=LIQUIDITY_WINDOWS,
        asset=symbol
    )

    return symbol, df_processed


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_data_processing_pipeline():

    print("\n========================================")
    print("DATA PROCESSING PIPELINE START")
    print("========================================\n")

    # --------------------------------------------------------
    # LOAD RAW DATA
    # --------------------------------------------------------

    assets = get_all_assets()

    print(f"Loading raw data for {len(assets)} assets...\n")

    raw_data = load_raw_dataset(assets)

    # --------------------------------------------------------
    # PROCESS DATA
    # --------------------------------------------------------

    processed_data = {}

    print("\nProcessing assets...\n")

    for asset in assets:

        symbol, df_processed = process_asset(asset, raw_data)

        processed_data[symbol] = df_processed

    # --------------------------------------------------------
    # SAVE PROCESSED DATA
    # --------------------------------------------------------

    save_processed_dataset(
        processed_data=processed_data,
        base_path=PROCESSED_DATA_PATH,
        columns=PROCESSED_COLUMNS
    )

    print("\n========================================")
    print("DATA PROCESSING PIPELINE COMPLETED")
    print("========================================\n")

    return processed_data