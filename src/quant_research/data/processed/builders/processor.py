# ============================================================
# PROCESSOR - PROCESSED DATA PIPELINE
# ============================================================


from quant_research.data.processed.transforms.transforms import process_asset_pipeline
from quant_research.data.processed.config.config import (
    RETURN_WINDOWS,
    LIQUIDITY_WINDOWS,
    
)
from quant_research.data.processed.validators.validators import (
    validate_expected_columns
)

def process_asset(asset, raw_data):

    symbol = asset.symbol

    print(f"\nProcessing asset: {symbol}")

    df_raw = raw_data[symbol]

    df_processed = process_asset_pipeline(
        df_raw.copy(),
        return_windows=RETURN_WINDOWS,
        liquidity_windows=LIQUIDITY_WINDOWS,
        asset=symbol
    )

    # --------------------------------------------------------
    # 🔥 VALIDATION (post-processing)
    # --------------------------------------------------------

    validate_expected_columns(df_processed, symbol)

    return symbol, df_processed

