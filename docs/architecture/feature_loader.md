# Feature Loader

## Overview

The Feature Loader is responsible for reading precomputed feature data from storage and providing a clean, consistent interface to access them.

It acts as the data access layer for feature data and is used by higher-level components such as the Panel Builder.

---

## Responsibilities

- Load feature data from parquet files
- Retrieve features by:
  - family
  - asset
  - date range (optional)
- Return standardized pandas DataFrames
- Provide a consistent and simple interface for downstream components

---

## Data Structure

Feature data is stored as parquet files following this convention:


data/features/asset/{family}/{asset}.parquet


### Example:


data/features/asset/momentum/SPY.parquet
data/features/asset/volatility/BTC.parquet


---

## File Format

Each parquet file contains:

- **Index**: datetime (asset-specific timeline)
- **Columns**: feature values

Example:

| datetime   | MOM_63 | MOM_252 |
|-----------|--------|---------|
| 2023-01-01 | 0.02   | 0.15    |

---

## Usage


from quant_research.features.loaders.feature_loader import FeatureLoader

loader = FeatureLoader()

df = loader.load_asset_features(
    family="momentum",
    asset="SPY",
    start="2020-01-01",
    end="2023-01-01"
)


Loading Process
---

1. Resolve file path using:

FEATURE_PATH / {family} / {asset}.parquet

2. Read parquet file into a pandas DataFrame

3. Apply optional filters:

- Date filtering (start, end)

- Column selection (optional, future extension)

4. Return the resulting DataFrame

---
Design Principles

1. Simplicity

The loader should remain minimal and focused only on reading data.

2. Determinism

Given the same inputs, the loader must always return the same output.

3. Statelessness

The loader does not store internal state or cache results (by default).

4. Separation of Concerns

The loader is strictly a data access layer and does not perform transformations.

Important Constraints
---
❌ The Feature Loader does NOT:

- Compute features
- Align calendars across assets
- Merge multiple assets
- Perform cross-sectional operations
- Handle advanced NaN logic (ffill, interpolation, etc.)
- Modify or transform feature values

✅ The Feature Loader ONLY:

- Reads feature data from disk
- Filters data by date (optional)
- Returns raw feature matrices

Relationship to Other Components

- Feature Registry → defines feature metadata and computation

- Feature Loader   → reads stored feature data

- Panel Builder    → aggregates data across assets and families

- Cross-Sectional Transformer → applies cross-asset transformations


Future Extensions
---
- Column-level filtering (load only selected features)

- Caching layer (in-memory or disk-based)

- Lazy loading

- Support for remote storage (S3, GCS, etc.)

- Versioned feature retrieval

Final Insight
---
The Feature Loader is the data boundary of the feature layer.

It ensures that all downstream components operate on a clean, consistent, and well-defined dataset, without introducing hidden transformations or side effects.