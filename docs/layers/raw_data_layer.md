# Raw Data Layer

## Overview

The Raw Data Layer is responsible for **ingesting, validating, and storing raw market data**.

It is the **entry point of the data pipeline**, providing a reproducible and consistent data foundation for all downstream processes.

---

## Responsibilities

The Raw Data Layer is responsible for:

- Downloading historical market data
- Performing basic data validation
- Enforcing a consistent schema across assets
- Storing data in a structured format

---

## Output

The layer produces:

- One dataset per asset
- Datetime-indexed data
- Standardized OHLCV schema

---

## Data Storage

Data is stored as:


`data/raw/{asset}.parquet`


Each file contains the full available history for a given asset.

---

## Schema Contract

All datasets must conform to the following structure:

```
Open
High
Low
Close
Adj Close
Volume
Dividends
Stock Splits
Capital Gains

```

Missing fields must be added during normalization.

---

## Key Properties

### Reproducibility

Datasets can be rebuilt from the original data source.

### Incremental Updates

Only new data is appended to existing datasets.

### Consistency

All assets share the same schema.

### Idempotency

Running the pipeline multiple times produces the same result.

---
## Temporal Integrity & Incremental Guarantees 

The raw data layer enforces **strict temporal consistency** across all assets.

### Effective Data Date (`effective_today`)

Each pipeline run defines a maximum valid timestamp:

- prevents usage of incomplete candles (e.g. crypto)
- aligns assets with different trading calendars
- acts as the **temporal boundary of the dataset**

---

### Temporal Enforcement

After every pipeline execution, datasets are **strictly bounded**:

```python
df = df[df.index <= effective_today]
```


This ensures:

- no future data leakage
- no partial candles
- no lookahead bias in downstream research

---

### Incremental Update Logic (Robust)

The pipeline follows a **state-based approach**:

- If no dataset exists → full download
- If dataset exists → incremental download
- If no new data → dataset is still validated and corrected

---

### Auto-Healing Property

Datasets are automatically corrected if inconsistencies are detected.

Example:

- crypto candle downloaded before close
- next pipeline run removes invalid data

This guarantees:

- long-term consistency
- no manual intervention
- stable research inputs

---

### Cross-Asset Consistency

Different asset classes behave differently:

- equities → discrete market close
- crypto → continuous trading

The pipeline normalizes this via `effective_today`, ensuring:

- aligned time series
- valid cross-asset comparisons
- consistent feature computation

---

### Extended Guarantees

In addition to the original properties, the layer now guarantees:

- temporal correctness
- cross-asset alignment
- deterministic dataset boundaries
- self-correcting behavior

---

## What This Layer Does NOT Do

The Raw Data Layer does NOT:

- Compute returns
- Engineer features
- Perform forward-looking transformations
- Apply statistical processing

These responsibilities belong to higher layers.

---

## Position in Architecture

```
Asset Universe
↓
Raw Data Layer
↓
Processed Data Layer
↓
Feature Layer
```

---

## Design Philosophy

The Raw Data Layer is intentionally minimal.

It preserves data as close as possible to the original source while ensuring:

- structural consistency
- data integrity
- usability for downstream pipelines