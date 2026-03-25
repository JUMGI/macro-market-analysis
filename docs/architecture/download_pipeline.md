# Download Pipeline

## Overview

The download pipeline is responsible for orchestrating the ingestion of raw market data.

It coordinates the interaction between:

- asset universe
- data source (yfinance)
- validation utilities
- storage layer

---

## Pipeline Flow

For each asset:

1. Determine last available date
2. Compute required download range
3. Download new data
4. Validate dataset
5. Normalize schema
6. Merge with existing data
7. Persist updated dataset

---

## Incremental Logic

The pipeline performs incremental updates:

- If no dataset exists → full download
- If dataset exists → download only new observations

This ensures efficiency and avoids redundant downloads.

---

## Temporal Handling (Critical)

### Effective Data Date

The pipeline introduces a **temporal control variable**:

```python
effective_today = get_effective_today(asset, end)
```

This represents the **latest valid data point** allowed in the dataset.

---

### Logical vs Physical Download Window

The pipeline distinguishes between:

**Logical window (desired data):**

```
start_date → effective_today
```


**Physical window (API requirement):**

```
start_date → effective_today + 1 day
```

(yfinance uses exclusive end dates)

---

## Robust Incremental Behavior

The pipeline separates data flows explicitly:

- `df_existing` → previously stored dataset
- `df_new` → newly downloaded data

Merge rules:

- no existing + no new → skip
- no existing → use new
- no new → use existing
- both → merge

---

## Temporal Integrity Enforcement

Unlike traditional pipelines, this system enforces:

```python
df = df[df.index <= effective_today]
```
**always**, regardless of whether new data was downloaded.

This ensures:

- no stale future data remains
- consistency across runs
- reproducibility of datasets

---

## Auto-Correction Mechanism

The pipeline is **self-healing**:

- incorrect rows (e.g. incomplete crypto candles)
- are automatically removed on subsequent runs

This avoids:

- hidden data corruption
- silent lookahead bias

---

## Improved Logging

The pipeline provides detailed logs per asset:

- effective data date
- last stored date
- incremental or full download
- logical download window
- number of downloaded rows
- trimming events
- final dataset state

Example:

```
Processing: BTC (BTC-USD)
Effective data date: 2026-03-23
Last stored date: 2026-03-24
Incremental from: 2026-03-25
⚠️ Trimmed 1 future rows
Final last stored date: 2026-03-23
```

---

## Design Upgrade

The pipeline evolved from:

- event-driven downloader
to:
- state-based data system

This means:

- outputs depend on dataset state, not just new events
- consistency is enforced every run
- datasets are guaranteed to converge to a valid state

---

## Components

### Universe Registry

Defines the set of assets processed by the pipeline.


`src/quant_research/data/registry/universe_registry.py`


---

### Helpers

Reusable functions used by the pipeline:

- data download
- validation
- normalization
- merging
- persistence


`src/quant_research/data/raw/helpers.py`


---

### Configuration

Centralized pipeline parameters:

- start date
- interval
- adjustment flags


`src/quant_research/data/raw/download_config.py`


---

### Pipeline Orchestrator

Main entry point:


`run_download_pipeline()`


Located in:


`src/quant_research/data/raw/download_pipeline.py`


---

## Execution

Typical usage:

```python
from quant_research.data.raw.download_pipeline import run_download_pipeline

run_download_pipeline()
```

Optional parameters allow:

subset of assets
custom date ranges
verbose logging control
---

## Logging

The pipeline controls logging and execution feedback.

Helpers are intentionally side-effect free.

---
## Design Decisions

### Asset Abstraction

All operations are based on structured `Asset` objects rather than raw strings.

### Separation of Concerns
- helpers = pure functions + IO
- pipeline = orchestration

### Deterministic Behavior

Pipeline outputs are deterministic given the same inputs.

## Future Extensions

The pipeline is designed to support:

- multiple data providers
- alternative storage backends
- parallel execution
- retry logic for failed downloads