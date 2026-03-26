# ============================================================
# PROCESSED DATA LAYER CONFIGURATION
# ============================================================

"""
Configuration module for the processed data pipeline.

This file defines:

1. Data schema (input + output)
2. Processing behavior (returns, corporate actions)
3. Core rolling window definitions

Design principles:

- Raw data is immutable
- Processing is deterministic and asset-local
- No cross-asset logic is defined here
- Missing data handling is deferred to later layers
"""

# ============================================================
# DATA SCHEMA
# ============================================================

# Expected columns in raw datasets
EXPECTED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "vendor_adj_close",
    "Volume",
    "Dividends",
    "Stock Splits",
    "Capital Gains"
]

# Core OHLC price columns
PRICE_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close"
]

# Corporate action fields
CORPORATE_ACTION_COLUMNS = [
    "Dividends",
    "Stock Splits",
    "Capital Gains"
]

# ============================================================
# PROCESSED DATASET COLUMNS
# ============================================================

PROCESSED_COLUMNS = [
    # --- Raw Market Data ---
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    # --- Vendor Reference ---
    "vendor_adj_close",

    # --- Corporate Actions ---
    "Dividends",
    "Capital Gains",
    "Stock Splits",

    # --- Total Return Construction ---
    "distribution",
    "dist_factor",
    "cum_adj_factor",
    "adj_close",

    # --- Returns ---
    "log_ret",
    "log_ret_5",
    "log_ret_21",
    "log_ret_63",
    "log_ret_126",
    "log_ret_252",

    # --- Liquidity ---
    "dollar_volume",
    "dollar_volume_21",
    "dollar_volume_63",
]

# ============================================================
# PROCESSING CONFIGURATION
# ============================================================

# Return calculation method
# Options (future): "log", "simple"
RETURN_TYPE = "log"

# Whether to include capital gains in total return adjustments
INCLUDE_CAPITAL_GAINS = True

# ============================================================
# WINDOW CONFIGURATION
# ============================================================

# Standard return horizons (trading days)
RETURN_WINDOWS = [5, 21, 63, 126, 252]

# Liquidity smoothing windows
LIQUIDITY_WINDOWS = [21, 63]

# ============================================================
# NOTES
# ============================================================

"""
Important architectural decisions:

- No forward/backward filling is applied in this layer
- Missing data is preserved intentionally
- Cross-asset alignment is handled in the systemic layer
- Returns are not filled (NaNs are expected at boundaries)

- 'vendor_adj_close' is preserved for validation purposes
- 'adj_close' is internally reconstructed using corporate actions
- Rolling features are treated as core derived fields (not full feature layer)

This ensures:

- Transparency of transformations
- Reproducibility of total return calculations
- Clean separation between data processing and feature engineering
"""