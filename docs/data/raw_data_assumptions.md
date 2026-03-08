# Raw Data Assumptions

This document defines the assumptions and rules applied to raw financial data in the Quant Research Platform.

## Data Type
- Daily adjusted close prices
- Multi-asset panel format (wide format by default)
- Assets include ETFs, equities, and crypto
- Crypto (e.g., BTC) may have 7-day trading; equities typically 5-day trading

## Return Construction
- Log returns are used:

\[
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
\]

**Reasons:**
- Additivity across time
- Statistical stability
- Symmetry properties

- Returns are computed **after price cleaning and calendar alignment**
- No forward filling of returns
- Rolling windows naturally introduce warm-up NaNs
- No artificial data imputation

## Missing Data Handling
- Assets may have different starting dates
- Calendar alignment uses **union of all dates**
- Forward-fill is applied **only to equities** (SPY, QQQ, XLE) with a **limit of 5 days** to cover weekends and holidays
- Crypto maintains real values on weekends; no artificial imputation
- Remaining NaNs at the start of series are dropped

## Alignment
- All assets aligned on a **full calendar date index**
- Missing dates for non-trading assets are handled by forward-fill (limited) or remain NaN if at start

## Time Horizon
- Daily frequency
- Horizons defined in trading days:
  - 21 ≈ 1 month
  - 63 ≈ 3 months
  - 126 ≈ 6 months
  - 252 ≈ 1 year

## Outliers
- No outlier removal at this stage
- Extreme returns remain, as volatility calculations rely on natural extremes

## Storage & Formats
- Processed datasets are stored in **Parquet format** for efficiency and reproducibility:
  - `prices.parquet`
  - `returns.parquet`
- Parquet allows fast loading for notebooks and research modules
- Versioning of processed datasets is recommended

## Future Extensions
- Intraday data
- High/Low range data
- Volume data
- Macro variables
- Transformations for ML (wide → long format)
