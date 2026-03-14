# Raw Market Data Pipeline

## Overview

This module implements the **raw market data ingestion layer** of the quant research framework.

Its purpose is to **download, validate, normalize, and store historical market data** in a local parquet data lake that can be used by research notebooks and feature engineering pipelines.

The design follows a layered architecture:

```
Asset Universe Registry
        ↓
Raw Data Download Pipeline
        ↓
Raw Data Validation & Normalization
        ↓
Parquet Data Lake (RAW_DATA_PATH)
```

This ensures that raw data is:

* reproducible
* incrementally updated
* stored in a consistent format
* easily accessible by higher layers of the research framework

---

# Data Storage

Raw market data is stored as **one parquet file per asset**:

```
RAW_DATA_PATH/

    SPY.parquet
    QQQ.parquet
    BTC.parquet
    GLD.parquet
    ...
```

Each dataset contains **daily OHLCV market data**.

### Expected schema

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

Some assets may not naturally contain all fields.
Missing fields are **automatically added during normalization** to guarantee a consistent schema across all assets.

---

# Asset Universe Registry

Assets used in the research environment are defined in:

```
src/quant_research/data/registry/universe_registry.py
```

The universe is implemented as a **list of Asset objects**.

Each asset contains:

* internal symbol
* external ticker (e.g. yfinance ticker)
* optional metadata

Example:

```
SPY = Asset(
    symbol="SPY",
    yfinance_ticker="SPY"
)
```

Example universe structure:

```
ASSET_UNIVERSE = [
    SPY,
    QQQ,
    BTC,
    GLD
]
```

This registry defines the **research universe used by the raw data pipeline**.

---

# Data Source

Historical market data is downloaded using:

```
yfinance
```

This provides access to data such as:

* US equities
* ETFs
* cryptocurrencies
* indices
* commodities

Example tickers:

```
SPY
QQQ
GLD
BTC-USD
ETH-USD
```

---

# Incremental Download Pipeline

The pipeline performs **incremental updates** rather than full downloads.

For each asset:

1. Check if a parquet dataset already exists
2. Detect the last stored date
3. Download only new data
4. Validate and normalize the dataset
5. Merge with existing data
6. Save updated dataset

Example output:

```
Processing asset: SPY
Last stored date: 2026-03-13
Downloaded rows: 1
Dataset rows after merge: 6588
```

If the dataset is already up to date:

```
Data already up to date
```

---

# Data Validation

Basic sanity checks are applied after download:

* ensure datetime index
* sort dataset chronologically
* remove duplicated timestamps

This keeps the raw dataset **as close as possible to the original data source**, while removing technical inconsistencies introduced during incremental downloads.

---

# Column Normalization

Different assets may contain different columns.

Example:

### SPY

```
Open High Low Close Adj Close Volume Dividends Stock Splits Capital Gains
```

### BTC

```
Open High Low Close Adj Close Volume Dividends Stock Splits
```

The pipeline **normalizes all datasets to a common schema**, automatically adding missing columns.

This guarantees **consistent data structures for downstream processing**.

---

# Data Quality Checks

Before using the dataset in research, the following checks are recommended:

### OHLC consistency

```
Low ≤ Open ≤ High
Low ≤ Close ≤ High
```

### Extreme return detection

Detect abnormal price jumps that may indicate bad data.

### Date gap analysis

Detect missing periods in the time series.

These checks are currently performed in the **research notebook layer** for exploratory validation.

---

# Raw Data Module Architecture

The raw data ingestion layer is implemented in:

```
src/quant_research/data/raw
```

```
raw/

    download_config.py
    download_pipeline.py
    raw_data_helpers.py
```

### download_config.py

Centralized configuration for the download pipeline:

```
START_DATE
INTERVAL
AUTO_ADJUST
ACTIONS
```

This isolates **pipeline parameters from pipeline logic**.

---

### raw_data_helpers.py

Contains reusable helper functions used by the pipeline:

* parquet existence checks
* last date detection
* asset download via yfinance
* dataset validation
* schema normalization
* dataset merging
* parquet persistence

These utilities keep the pipeline implementation clean and modular.

---

### download_pipeline.py

Orchestrates the complete raw data ingestion process.

Main responsibilities:

* iterate through `ASSET_UNIVERSE`
* perform incremental downloads
* call validation and normalization helpers
* merge with existing datasets
* persist datasets to the parquet data lake

The pipeline is exposed through:

```
run_download_pipeline()
```

---

# Notebook Execution Layer

Research notebooks execute the pipeline through a simple interface:

```
from quant_research.data.raw.download_pipeline import run_download_pipeline

run_download_pipeline()
```

This keeps notebooks **lightweight orchestration layers**, while the data logic resides in the source code.

---

# Current Architecture Status

The following components are implemented:

```
src/quant_research

data/
    registry/
        universe_registry.py

    raw/
        download_config.py
        download_pipeline.py
        raw_data_helpers.py
```

This completes the **Raw Data Layer** of the research architecture.

---

# Next Steps

The next architectural component is the **Market Data Loader**:

```
data/loaders/market_data_loader.py
```

This module will provide a clean interface for loading datasets from the parquet data lake.

Example usage:

```
spy = load_asset("SPY")
btc = load_asset("BTC")
```

This abstraction allows the **research layer to remain independent from the storage backend**.

---

# Design Philosophy

The data pipeline follows several principles.

### Reproducibility

All datasets can be rebuilt from source.

### Incremental updates

Only new market data is downloaded.

### Storage simplicity

Raw data is stored as **parquet files per asset**.

### Separation of concerns

Data ingestion is separated from:

* feature engineering
* research notebooks
* modeling pipelines

This architecture **scales naturally as the research framework grows**.
