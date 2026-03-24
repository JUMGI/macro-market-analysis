# ============================================================
# RAW MARKET DATA DOWNLOAD PIPELINE
# ============================================================

from datetime import datetime, timedelta
from typing import Optional, List

from quant_research.data.registry.universe_registry import ASSET_UNIVERSE, Asset

from quant_research.data.raw.helpers import (
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
    ACTIONS,
)


# ============================================================
# Pipeline
# ============================================================

def run_download_pipeline(
    assets: Optional[List[Asset]] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    verbose: bool = True,
):
    """
    Run raw data download pipeline.

    Parameters
    ----------
    assets : list[Asset], optional
        Subset of assets to process (default: full universe)
    start : str, optional
        Override global START_DATE
    end : str, optional
        End date (default: today)
    verbose : bool
        Enable logging
    """

    assets = assets or ASSET_UNIVERSE
    today = end or datetime.today().strftime("%Y-%m-%d")
    global_start = start or START_DATE

    if verbose:
        print("\n=== RAW DATA DOWNLOAD PIPELINE ===\n")

    # ========================================================
    # Loop over assets
    # ========================================================

    for asset in assets:

        symbol = asset.symbol
        ticker = asset.get_ticker()

        if verbose:
            print(f"Processing: {symbol} ({ticker})")

        # ----------------------------------------------------
        # Determine start date
        # ----------------------------------------------------

        last_date = get_last_date(asset)

        if last_date is None:
            start_date = global_start

            if verbose:
                print(f"  No existing data → full download from {start_date}")

        else:
            start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")

            if verbose:
                print(f"  Last stored date: {last_date.date()}")
                print(f"  Incremental download from {start_date}")

        # ----------------------------------------------------
        # Skip if already up to date
        # ----------------------------------------------------

        if start_date > today:
            if verbose:
                print("  Up to date\n")
            continue

        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        df = download_asset(
            asset=asset,
            start_date=start_date,
            end_date=today,
            interval=INTERVAL,
            auto_adjust=AUTO_ADJUST,
            actions=ACTIONS,
        )

        if df.empty:
            if verbose:
                print("  No new data\n")
            continue

        if verbose:
            print(f"  Downloaded rows: {len(df)}")

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        df = validate_download(df)

        # ----------------------------------------------------
        # Normalize schema
        # ----------------------------------------------------

        df = normalize_columns(df)

        # ----------------------------------------------------
        # Merge with existing
        # ----------------------------------------------------

        df = merge_with_existing(df, asset)

        if verbose:
            print(f"  Total rows after merge: {len(df)}")

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        save_parquet(df, asset)

        if verbose:
            print("  Saved\n")

    if verbose:
        print("=== PIPELINE FINISHED ===\n")