# ============================================================
# RAW MARKET DATA DOWNLOAD PIPELINE (1D - FINAL STABLE)
# ============================================================

from datetime import datetime
from typing import Optional, List
import pandas as pd

from quant_research.config.paths import RAW_DATA_PATH

from quant_research.data.registry.universe_registry import get_all_assets, Asset

from quant_research.data.raw.utils.helpers import (
    get_last_date,
    validate_download,
    normalize_columns,
    merge_with_existing,
    
)
from quant_research.data.raw.sources.yahoo import download_ohlcv

from quant_research.data.raw.utils.io import save_parquet

from quant_research.data.raw.utils.time import get_effective_today

from quant_research.data.raw.config.download_config import (
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
    Stable 1D raw data pipeline.

    Guarantees:
    - no lookahead bias
    - consistent temporal cutoff
    - safe incremental updates
    - automatic data correction (trimming)
    """

    assets = assets if assets is not None else get_all_assets()
    global_start = pd.to_datetime(start or START_DATE)

    if verbose:
        print("\n=== RAW DATA DOWNLOAD PIPELINE ===\n")

    # ========================================================
    # Loop
    # ========================================================

    for asset in assets:

        symbol = asset.symbol
        ticker = asset.get_ticker()

        # ----------------------------------------------------
        # Temporal truth
        # ----------------------------------------------------

        effective_today = get_effective_today(asset, end)
        download_end = effective_today + pd.Timedelta(days=1)  # yfinance exclusive

        if verbose:
            print(f"Processing: {symbol} ({ticker})")
            print(f"  Effective data date: {effective_today.date()}")

        # ----------------------------------------------------
        # Load existing dataset (if any)
        # ----------------------------------------------------

        path = RAW_DATA_PATH / f"{symbol}.parquet"

        if path.exists():
            df_existing = pd.read_parquet(path)
            last_date = df_existing.index.max()
        else:
            df_existing = None
            last_date = None

        # ----------------------------------------------------
        # Determine start date
        # ----------------------------------------------------

        if last_date is None:
            start_date = global_start

            if verbose:
                print("  Last stored date: NONE")
                print(f"  Full download from: {start_date.date()}")

        else:
            start_date = last_date + pd.Timedelta(days=1)

            if verbose:
                print(f"  Last stored date: {last_date.date()}")
                print(f"  Incremental from: {start_date.date()}")

        # ----------------------------------------------------
        # Download if needed
        # ----------------------------------------------------

        df_new = pd.DataFrame()

        if start_date <= effective_today:

            if verbose:
                print(f"  Download window (logical): {start_date.date()} → {effective_today.date()}")

            df_new = download_ohlcv(
                asset=asset,
                start_date=start_date,
                end_date=download_end,
                interval=INTERVAL,
                auto_adjust=AUTO_ADJUST,
                actions=ACTIONS,
            )

            if not df_new.empty:
                if verbose:
                    print(f"  Downloaded rows: {len(df_new)}")

                df_new = validate_download(df_new)
                df_new = normalize_columns(df_new)

        else:
            if verbose:
                print("  Up to date")

        # ----------------------------------------------------
        # Merge logic
        # ----------------------------------------------------

        if df_existing is None and df_new.empty:
            if verbose:
                print("  No data available\n")
            continue

        if df_existing is None:
            df = df_new

        elif df_new.empty:
            df = df_existing

        else:
            df = merge_with_existing(df_new, asset)

        # ----------------------------------------------------
        # 🔥 ALWAYS enforce temporal integrity
        # ----------------------------------------------------

        before_rows = len(df)

        df = df[df.index <= effective_today]

        after_rows = len(df)

        # ----------------------------------------------------
        # Logging after trimming
        # ----------------------------------------------------

        if verbose:

            if after_rows < before_rows:
                print(f"  ⚠️ Trimmed {before_rows - after_rows} future rows")

            final_last_date = df.index.max()

            print(f"  Final last stored date: {final_last_date.date()}")
            print(f"  Total rows: {len(df)}")

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        save_parquet(df, asset)

        if verbose:
            print("  Saved\n")

    if verbose:
        print("=== PIPELINE FINISHED ===\n")