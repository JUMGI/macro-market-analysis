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