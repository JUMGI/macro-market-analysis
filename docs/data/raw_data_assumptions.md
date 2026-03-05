# Raw Data Assumptions

This document defines assumptions about raw financial data.

---

## Data Type

- Daily adjusted close prices
- Multi-asset panel format
- Assets may include ETFs, equities, crypto

---

## Return Construction

Log returns are used:

r_t = log(P_t / P_{t-1})

Reason:
- Additivity across time
- Statistical stability
- Symmetry properties

---

## Missing Data Handling

- Assets may have different starting dates.
- No forward filling of returns.
- Rolling windows naturally introduce warm-up NaNs.
- No artificial data imputation.

---

## Alignment

All assets are aligned on calendar date index.

If an asset does not trade on a given date:
- That date remains NaN for that asset.

No artificial synchronization.

---

## Time Horizon

- Daily frequency.
- Horizons defined in trading days:
    - 21 ≈ 1 month
    - 63 ≈ 3 months
    - 126 ≈ 6 months
    - 252 ≈ 1 year

---

## Outliers

No outlier removal at this stage.
Volatility captures extreme behavior by design.

---

## Future Extensions

Possible additions:
- Intraday data
- High/Low range data
- Volume data
- Macro variables
