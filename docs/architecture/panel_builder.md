# Panel Builder

## Overview
The **Panel Builder** is responsible for constructing cross-asset feature datasets from precomputed feature data.

It aggregates features across assets and families, aligns them in time, and applies optional post-processing such as NaN handling and structural formatting.

It serves as the **dataset construction layer** for research workflows.

---

## Responsibilities
* **Data Loading:** Via the Feature Loader.
* **Aggregation:** Combines features across multiple assets and feature families.
* **Time Alignment:** Synchronizes time series across different assets.
* **Contract Enforcement:** Ensures a standardized panel structure independent of internal implementation.
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
3. Align and concatenate across assets.
4. Enforce panel contract (structure normalization).
5. Apply structural formatting.
6. Apply NaN handling policy.
7. Return final dataset.

---

## Panel Contract (Canonical Structure)

The Panel Builder enforces a standardized output structure:

**Index**
* Datetime index

**Columns (MultiIndex)**
* Level 0 → `feature`
* Level 1 → `asset`

**Column Names**
* `["feature", "asset"]`

This contract guarantees:

* Consistent slicing semantics
* Stable downstream APIs
* Independence from alignment implementation details

---

## Configuration Parameters

### Assets
List of asset symbols (e.g., SPY, BTC).

### Families
List of feature families (e.g., momentum, volatility).

### Start / End
Optional date filters applied before panel construction.

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
* **MultiIndex (default):** `(feature, asset)` format.
* **Flat:** `ASSET_FEATURE` naming convention (wide format).

---

## Output Structure (Examples)

### MultiIndex (Canonical)


| date | (MOM_63, SPY) | (MOM_63, BTC) |
| :--- | :--- | :--- |
| 2023-01-01 | 0.05 | 0.12 |

---

### Flat (Wide Format)


| date | SPY_MOM_63 | BTC_MOM_63 |
| :--- | :--- | :--- |
| 2023-01-01 | 0.05 | 0.12 |

> Note: Flat structure is still a **wide format**, not a long/tidy dataset.

---

## Design Principles
1. **Separation of Concerns:** Panel Builder does not compute features or read raw data.
2. **Contract-Driven Design:** Output structure is explicitly enforced via panel contracts.
3. **Flexibility:** Users control alignment strategy, NaN handling, and structure.
4. **Transparency:** NaNs are preserved by default.
5. **Determinism:** Given the same inputs, the output panel is identical.

---

## Execution Logging
Each panel build reports:
* Assets used
* Feature families
* Dimensions (rows × columns)
* Effective date range
* NaN percentage
* Alignment method applied

---

## Important Insights
* **NaNs are expected:** They arise from different trading calendars and rolling windows.
* **Alignment is a research decision:** Intersection yields cleaner datasets; Union preserves full information.
* **Contract enforcement is critical:** It guarantees consistency regardless of how data is internally aligned.
* **Wide vs Long:** The panel is designed as a wide dataset; long format transformations are performed downstream when needed.

---

## Key Insight
The Panel Builder is the **bridge between feature computation and research**.

It transforms isolated per-asset feature datasets into a unified, structured representation of the market suitable for:

* Cross-asset analysis
* Regime detection
* Machine learning
* Systematic allocation research