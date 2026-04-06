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

PRICE_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close"
]

CORPORATE_ACTION_COLUMNS = [
    "Dividends",
    "Stock Splits",
    "Capital Gains"
]

# ============================================================
# WINDOW CONFIGURATION (🔥 SINGLE SOURCE OF TRUTH)
# ============================================================

# Return horizons (trading days)
RETURN_WINDOWS = [5, 21, 63, 126, 252]

# Liquidity smoothing windows
LIQUIDITY_WINDOWS = [21, 63]

# ============================================================
# PROCESSED DATASET COLUMNS (🔥 WINDOW-DRIVEN)
# ============================================================

"""
Defines the exact schema exported to parquet.

Structure:
- Static core columns
- Dynamic return columns (based on RETURN_WINDOWS)
- Dynamic liquidity columns (based on LIQUIDITY_WINDOWS)
"""

# --- Static blocks
_BASE_COLUMNS = [
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
]

# --- Returns (🔥 dynamic)
_RETURN_COLUMNS = ["log_ret"] + [f"log_ret_{w}" for w in RETURN_WINDOWS]

# --- Liquidity (🔥 dynamic)
_LIQUIDITY_COLUMNS = ["dollar_volume"] + [f"dollar_volume_{w}" for w in LIQUIDITY_WINDOWS]

# --- Final schema
PROCESSED_COLUMNS = (
    _BASE_COLUMNS
    + _RETURN_COLUMNS
    + _LIQUIDITY_COLUMNS
)

# ============================================================
# PRIMITIVE FEATURES (🔥 DOWNSTREAM CONTRACT)
# ============================================================

"""
Primitive features exposed to downstream layers (systemic, regimes).

Includes:
- price proxy (adj_close)
- returns (all horizons)
- liquidity proxies
"""

PRIMITIVE_FEATURES = (
    ["adj_close"]
    + _RETURN_COLUMNS
    + _LIQUIDITY_COLUMNS
)

# ============================================================
# FEATURE NAMING NORMALIZATION (🔥 CRITICAL)
# ============================================================

"""
Maps internal column names → standardized feature names.

Naming convention:
- RET_h → returns
- DV_h  → dollar volume
- PRICE → adjusted price
"""

PROCESSED_FEATURE_MAP = {}

# --- Returns → RET_h
PROCESSED_FEATURE_MAP["log_ret"] = "RET_1"

for w in RETURN_WINDOWS:
    PROCESSED_FEATURE_MAP[f"log_ret_{w}"] = f"RET_{w}"

# --- Liquidity → DV_h
PROCESSED_FEATURE_MAP["dollar_volume"] = "DV_1"

for w in LIQUIDITY_WINDOWS:
    PROCESSED_FEATURE_MAP[f"dollar_volume_{w}"] = f"DV_{w}"

# --- Price
PROCESSED_FEATURE_MAP["adj_close"] = "PRICE"

# ============================================================
# PROCESSING CONFIGURATION
# ============================================================

# Return calculation method
# Options (future): "log", "simple"
RETURN_TYPE = "log"

# Whether to include capital gains in total return adjustments
INCLUDE_CAPITAL_GAINS = True

# ============================================================
# NOTES
# ============================================================

"""
Important architectural decisions:

- PROCESSED_COLUMNS is dynamically built but deterministic
- Window definitions are the single source of truth
- PRIMITIVE_FEATURES defines what downstream layers can use
- PROCESSED_FEATURE_MAP ensures naming consistency system-wide

- No forward/backward filling is applied in this layer
- Missing data is preserved intentionally
- Cross-asset alignment is handled in later layers
- Returns are not filled (NaNs expected at boundaries)

Layer responsibilities:

Processed Layer:
    - builds total return series
    - computes returns (RET_h)
    - computes liquidity (DV_h)

Feature Layer:
    - computes transforms (MOM, VOL, etc.)

Systemic Layer:
    - aggregates cross-asset behavior

This ensures:

- no duplicated computations (RET computed once)
- consistent naming across layers
- reproducibility and auditability
"""