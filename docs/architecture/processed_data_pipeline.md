# Processed Data Pipeline

## Overview

The Processed Data Pipeline orchestrates the transformation of raw market data into processed datasets.

It is responsible for:

- loading raw data
- applying transformations
- enforcing schema consistency
- saving processed datasets

---

## Pipeline Structure

The pipeline follows a modular architecture:

```
processor.py (orchestration)
↓
loaders.py (data loading)
↓
transforms.py (data transformations)
↓
io.py (data persistence)`
```


---

## Execution Flow

### 1. Load Asset Universe

Assets are retrieved from the registry:

```python
assets = get_all_assets()
```
---
### 2. Load Raw Data

Raw datasets are loaded into memory:

```pytho
raw_data = load_raw_dataset(assets)
```

Each dataset:

- corresponds to one asset
- is stored in a dictionary keyed by symbol

---
### 3. Process Each Asset

Each asset is processed independently:

```python
df_processed = process_asset_pipeline(df_raw)
```
---
### 4. Save Processed Data

Processed datasets are saved incrementally:
```python
save_processed_dataset(processed_data)
```
---
## Core Modules
`loaders.py`

Responsible for:

- reading parquet files from raw data
- returning a dictionary of DataFrames

`transforms.py`

Contains all transformation logic:

Raw Normalization
- normalize_raw_data
- ensure_corporate_action_columns
- remove_duplicate_index

Corporate Actions
- compute_distribution
- compute_dist_factor
- compute_cum_adj_factor
- compute_adj_close

Returns
- compute_log_returns
- compute_multi_horizon_returns
- Liquidity
- compute_dollar_volume
- compute_rolling_liquidity

Utilities
- clean_columns_metadata
- enforce_column_order

Full Pipeline
- process_asset_pipeline

`io.py`

Handles persistence:

Incremental Save
- merges new and existing data
- removes duplicate timestamps
- keeps latest observation

Properties
- idempotent
- robust to re-runs
- consistent across assets

`processor.py`

Orchestrates the full pipeline:

- loads assets
- loads raw data
- processes each asset
- saves results

---
## Incremental Update Logic

When saving processed data:

1. If dataset exists:
- load existing data
- concatenate with new data
- remove duplicate timestamps (keep latest)
- sort chronologically
2. If dataset does not exist:
- create new dataset

---
## Schema Enforcement

Before saving:

- all required columns are enforced
- missing columns are added as NaN
- column order is standardized

This guarantees:

- consistency across assets
- compatibility with downstream layers

---
## Output

Processed datasets are stored in:

`data/processed/{asset}.parquet`

Each dataset is:

- chronologically ordered
- schema-consistent
- ready for research use

---
## Logging

The pipeline logs:

-  asset processing steps
- dataset creation or update
- pipeline start and completion

---
## Design Properties

The pipeline is:

### Deterministic

`Same input → same output`

### Idempotent

Safe to run multiple times without corrupting data

### Modular

Each component is isolated and reusable

### Scalable

Supports larger asset universes without redesign

---
## Future Extensions

This pipeline can be extended with:

- parallel processing
- data validation hooks (audit layer)
- caching mechanisms
- versioned datasets