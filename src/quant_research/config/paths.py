from pathlib import Path

# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# macro-market-analysis/

# ============================================================
# Data paths
# ============================================================

DATA_PATH = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"

FEATURES_PATH = DATA_PATH / "features"

ASSET_FEATURE_PATH = FEATURES_PATH / "asset"

# ============================================================
# Feature families
# ============================================================

MOMENTUM_FEATURE_PATH = ASSET_FEATURE_PATH / "Momentum"
VOLATILITY_FEATURE_PATH = ASSET_FEATURE_PATH / "Volatility"
