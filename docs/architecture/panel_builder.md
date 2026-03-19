# Panel Builder

## Overview
The **Panel Builder** is responsible for constructing multi-asset feature datasets from precomputed feature data. 

It aggregates features across assets and families, aligns them in time, and applies optional post-processing such as NaN handling and structural formatting. It serves as the **dataset construction layer** for research workflows.

---

## Responsibilities
* **Data Loading:** Via the Feature Loader.
* **Aggregation:** Combines features across multiple assets and feature families.
* **Time Alignment:** Synchronizes time series across different assets.
* **NaN Management:** Applies configurable handling policies for missing values.
* **Structuring:** Provides flexible output formats for downstream research.

---

## Role in Architecture
**Feature Registry** → **Feature Loader** → **Panel Builder** → **Research / Models**

* **Feature Registry:** Defines feature metadata and computation.
* **Feature Loader:** Reads stored feature data.
* **Panel Builder:** Constructs research-ready datasets.
* **Research Layer:** Analysis, modeling, and backtesting.

---

## Data Flow
1. Load feature data per asset and family.
2. Merge features within each asset.
3. Merge assets into a unified panel.
4. Apply structural formatting.
5. Apply NaN handling policy.
6. Return final dataset.

---

## Configuration Parameters

### Assets
List of asset tickers (e.g., SPY, BTC).

### Families
List of feature families (e.g., momentum, volatility).

### Start / End
Optional date filters applied at the panel level.

### Alignment
Defines how time series are aligned:
* **Intersection:** Only common dates across assets (inner join).
* **Union:** All dates across assets (outer join).

### NaN Policy
Defines how missing values are handled:
* **Keep:** Preserve NaNs (recommended for research).
* **Drop:** Remove rows with any NaNs.
* **Ffill:** Forward fill missing values.
* **Bfill:** Backward fill missing values.

### Structure
Defines column structure:
* **MultiIndex:** (asset, feature) format.
* **Flat:** asset_feature naming convention.

---

## Output Structure (Examples)

### MultiIndex (Default)


| date | (SPY, MOM_63) | (BTC, MOM_63) |
| :--- | :--- | :--- |
| 2023-01-01 | 0.05 | 0.12 |

### Flat


| date | SPY_MOM_63 | BTC_MOM_63 |
| :--- | :--- | :--- |
| 2023-01-01 | 0.05 | 0.12 |

---

## Design Principles
1. **Separation of Concerns:** Panel Builder does not compute features or read raw data; it only constructs datasets.
2. **Flexibility:** Users control alignment strategy, NaN handling, and structure.
3. **Transparency:** No hidden transformations. NaNs are exposed by default.
4. **Determinism:** Given the same inputs, the output panel is always identical.

---

## Execution Logging
Each panel build reports:
* Assets used.
* Feature families.
* Dimensions (rows × columns).
* Effective date range.
* NaN percentage.
* Alignment method applied.

---

## Important Insights
* **NaNs are expected:** They arise from different trading calendars or rolling window "warmup" periods.
* **Alignment is a research decision:** Intersection provides a cleaner dataset with less data; Union provides the full dataset with more NaNs.
* **The Definitive Bridge:** The Panel Builder transforms isolated feature computations into a unified, structured dataset suitable for systematic analysis.



