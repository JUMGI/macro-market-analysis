# ============================================================
# RAW MARKET DATA DOWNLOAD PIPELINE
# ============================================================

from datetime import datetime, timedelta

from quant_research.data.registry.universe_registry import ASSET_UNIVERSE
from quant_research.data.raw.raw_data_helpers import (
    get_last_date,
    download_asset,
    validate_download,
    normalize_columns,
    merge_with_existing,
    save_parquet,
)

from quant_research.data.raw.download_config import (
    START_DATE,
    INTERVAL,
    AUTO_ADJUST,
    ACTIONS
)


# ------------------------------------------------------------
# Run download pipeline
# ------------------------------------------------------------

def run_download_pipeline():

    print("\nStarting raw market data download pipeline...\n")

    today = datetime.today().strftime("%Y-%m-%d")

    for asset in ASSET_UNIVERSE:

        symbol = asset.symbol
        ticker = asset.get_ticker()

        print(f"Processing asset: {symbol} ({ticker})")

        # ----------------------------------------------------
        # Determine start date
        # ----------------------------------------------------

        last_date = get_last_date(symbol)

        if last_date is None:

            start_date = START_DATE
            print(f"  No existing data. Downloading full history from {start_date}")

        else:

            start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"  Last stored date: {last_date.date()}")

        # ----------------------------------------------------
        # Skip if already up to date
        # ----------------------------------------------------

        if start_date > today:

            print("  Data already up to date.\n")
            continue

        # ----------------------------------------------------
        # Download new data
        # ----------------------------------------------------

        df = download_asset(
            asset,
            start_date=start_date,
            end_date=today,
            interval=INTERVAL,
            auto_adjust=AUTO_ADJUST,
            actions=ACTIONS
        )

        if df.empty:

            print("  No new data downloaded.\n")
            continue

        print(f"  Downloaded rows: {len(df)}")

        # ----------------------------------------------------
        # Validate dataset
        # ----------------------------------------------------

        df = validate_download(df)

        # ----------------------------------------------------
        # Normalize schema
        # ----------------------------------------------------

        df = normalize_columns(df)

        # ----------------------------------------------------
        # Merge incremental data
        # ----------------------------------------------------

        df = merge_with_existing(df, symbol)

        print(f"  Dataset rows after merge: {len(df)}")

        # ----------------------------------------------------
        # Save dataset
        # ----------------------------------------------------

        save_parquet(df, symbol)

        print()

    print("Download pipeline finished.\n")