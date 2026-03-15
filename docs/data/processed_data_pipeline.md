# Processed Market Data Pipeline

## Overview
This document describes the processing pipeline applied to raw market data
to produce clean, canonical datasets suitable for research and feature engineering.

The pipeline reads raw data downloaded from yfinance, applies corporate action adjustments,
calculates log returns, and generates liquidity metrics.

Processed datasets are stored per asset in:

data/processed/{asset}.parquet

---

## Pipeline Steps

### 1. Load Raw Data
- Read raw market data from parquet files: `data/raw/{asset}.parquet`.
- Ensure datetime index and chronological sorting.
- Remove duplicated timestamps if present.

### 2. Data Validation
- Check for missing or malformed values.
- Verify columns exist: Open, High, Low, Close, Adj Close, Volume, Dividends, Stock Splits, Capital Gains.

### 3. Corporate Action Adjustment
- Compute adjustment factors for:
    - Stock splits
    - Dividends
    - Capital gains
- Construct **adjusted close price** (`adj_close`) as the point-in-time correct price.

\[
adj\_close_t = Close_t \times \prod_{s \ge t} split\_factor_s \times div\_factor_s \times capgain\_factor_s
\]

- Note: `adj_close` differs from yfinance `Adj Close` in that all corporate actions are applied manually and verified.

### 4. Log Returns
- Logarithmic returns are computed for each asset using adjusted close prices:

\[
log\_ret_t = \ln\left(\frac{adj\_close_t}{adj\_close_{t-1}}\right)
\]

- Returns are aligned with the asset's own calendar to avoid look-ahead bias.

### 5. Liquidity Metrics
- Dollar volume per day:

\[
dollar\_volume_t = adj\_close_t \times Volume_t
\]

- Rolling averages computed over multiple windows (e.g., 21, 63 days) for research features.

### 6. Incremental Save
- Each processed dataset is saved per asset in parquet format.
- Incremental updates ensure that only new data is appended.
- Duplicate indices are removed before saving.

### 7. Processed Dataset Schema
Each processed dataset contains the following columns:

- Open
- High
- Low
- Close
- vendor_adj_close (original vendor-adjusted price from yfinance)
- Volume
- Dividends
- Stock Splits
- Capital Gains
- distribution
- dist_factor
- cum_adj_factor
- adj_close
- log_ret
- log_ret_X (rolling log returns over X days)
- dollar_volume
- dollar_volume_X (rolling dollar volume over X days)

---

## Notes

- All adjustments are applied **backward in time** to preserve point-in-time correctness.
- Log returns use adjusted prices and are the canonical representation for downstream features.
- Each asset uses its own calendar; weekends, holidays, and missing days are handled appropriately.
- Visual audits and basic diagnostics (e.g., jumps in adjusted prices) are recommended.
- Cross-asset alignment is deferred to the systemic feature layer.

---

## References

- Raw Market Data Pipeline: `00_download_market_data.ipynb`
- Universe Registry: `src/quant_research/data/registry/universe_registry.py`