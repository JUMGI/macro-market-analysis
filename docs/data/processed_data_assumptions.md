# Processed Data Assumptions

This document defines the rules and assumptions applied to **processed market datasets** in the Quant Research Platform.

These datasets are the output of the **01_data_pipeline.ipynb** notebook and are used for feature engineering, modeling, and research.

---

## Data Structure

- **Format:** Wide panel by default (index = date, columns = assets)
- **Assets:** ETFs, equities, crypto
- **Price type:** Adjusted close prices
- **Returns:** Log returns
- **File formats:** Parquet (`prices.parquet`, `returns.parquet`)
- **Calendar:** Daily, full union of all asset dates

Example wide format:

| Date       | BTC    | SPY    | QQQ    | XLE    |
|------------|--------|--------|--------|--------|
| 2015-01-01 | ...    | ...    | ...    | ...    |
| 2015-01-02 | ...    | ...    | ...    | ...    |

---

## Price Cleaning

- Prices are **sorted chronologically**
- **Forward-fill** applied **only to equities** (SPY, QQQ, XLE)  
  - Limit = 5 days (covers weekends + US market holidays)  
- **Crypto assets** (BTC) maintain real prices on weekends; no ffill  
- Initial NaNs after reindexing are dropped
- No other imputation is performed

---

## Calendar Alignment

- **All dates from the union of all asset calendars are included**  
- Missing equity prices are filled forward (limit=5)  
- Missing crypto dates are left as NaN if at the start, or filled naturally by reindexing  
- Ensures that datasets are **consistent for cross-asset analysis and ML pipelines**

---

## Return Computation

- **Log returns** are computed after price cleaning and alignment:

\[
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
\]

- Returns inherit the wide panel structure
- No forward-filling of returns
- Rolling windows may introduce warm-up NaNs naturally

---

## Diagnostics / Validation

- **Monotonic index check**: ensures chronological ordering  
- **No remaining NaNs** after initial cleaning  
- **Extreme returns** remain, as volatility measures rely on real data  
- Shape of datasets and asset columns are validated before export

---

## Storage & Versioning

- Stored in **Parquet format** for efficiency and reproducibility
- Recommended folder: `data/processed/`
- Filenames:  
  - `prices.parquet` → cleaned price series  
  - `returns.parquet` → log returns
- Version control via Git or dataset versioning tools (future extension)

---

## Time Horizon

- Daily frequency
- Horizons defined in trading days:  
  - 21 ≈ 1 month  
  - 63 ≈ 3 months  
  - 126 ≈ 6 months  
  - 252 ≈ 1 year

---

## Notes / Future Extensions

- Convert wide → long format for ML pipelines  
- Add new asset classes (bonds, FX, commodities)  
- Include additional data sources (volume, high/low, macro variables)  
- Integration with feature registry for automatic feature calculation
