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