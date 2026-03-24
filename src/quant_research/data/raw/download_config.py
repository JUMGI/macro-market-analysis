# ============================================================
# RAW DATA DOWNLOAD CONFIG
# ============================================================

START_DATE = "2000-01-01"

INTERVAL = "1d"

AUTO_ADJUST = False

ACTIONS = True

# ============================================================
# DATA AVAILABILITY POLICY
# ============================================================

"""
Daily data is considered FINAL after 01:00 UTC of the next day.

This ensures:
- Crypto candles are fully closed
- Equity markets are fully settled
- No partial/incomplete data is ingested
"""

DATA_AVAILABLE_HOUR_UTC = 1