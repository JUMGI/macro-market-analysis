from pathlib import Path
import pandas as pd
from quant_research.data.processed.transforms import enforce_column_order

def load_raw_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)

def save_processed_asset(
    df_new: pd.DataFrame,
    path: Path
):
    """
    Save processed dataset with incremental merge.
    """

    df_new = df_new.sort_index()

    # --------------------------------------------------------
    # MERGE WITH EXISTING
    # --------------------------------------------------------

    if path.exists():

        df_existing = pd.read_parquet(path)

        df_combined = pd.concat([df_existing, df_new])

        # remove duplicate timestamps (keep latest)
        df_combined = df_combined[~df_combined.index.duplicated(keep="last")]

        df_combined = df_combined.sort_index()

        df_combined.to_parquet(path)

        return "updated"

    # --------------------------------------------------------
    # FIRST SAVE
    # --------------------------------------------------------

    else:

        df_new.to_parquet(path)

        return "created"
    
def save_processed_dataset(processed_data, base_path, columns):

    print("\nSaving processed datasets...\n")

    for symbol, df in processed_data.items():

        output_path = base_path / f"{symbol}.parquet"

        # enforce schema
        df = enforce_column_order(df, columns)

        status = save_processed_asset(df, output_path)

        print(f"{status.capitalize()}: {symbol} → {output_path}")

    print("\nProcessed datasets saved successfully.")