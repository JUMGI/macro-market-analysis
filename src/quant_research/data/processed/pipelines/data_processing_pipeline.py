# data/processed/pipelines/data_processing_pipeline.py

from quant_research.config.paths import PROCESSED_DATA_PATH
from quant_research.data.registry.universe_registry import get_all_assets

from quant_research.data.raw.loaders.asset_raw_loader import (
    AssetRawDataLoader
)

from quant_research.data.processed.builders.processor import process_asset

from quant_research.data.processed.io.io import save_processed_dataset

from quant_research.data.processed.config.config import PROCESSED_COLUMNS


def run_data_processing_pipeline():

    print("\n========================================")
    print("DATA PROCESSING PIPELINE START")
    print("========================================\n")

    assets = get_all_assets()

    # --------------------------------------------------------
    # LOAD RAW DATA (from RAW layer)
    # --------------------------------------------------------

    loader = AssetRawDataLoader()
    raw_data = loader.load_universe(assets)

    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------

    processed_data = {}

    print("\nProcessing assets...\n")

    for asset in assets:

        symbol, df_processed = process_asset(asset, raw_data)

        processed_data[symbol] = df_processed

    # --------------------------------------------------------
    # SAVE
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