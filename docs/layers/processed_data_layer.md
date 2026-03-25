# Processed Data Layer

## Overview

The Processed Data Layer transforms raw market data into a **clean, consistent, and research-ready dataset**.

It serves as the **canonical data foundation** for all downstream components:

- feature engineering
- cross-asset analysis
- regime detection
- portfolio construction

---

## Objectives

The layer is designed to:

- remove inconsistencies from raw vendor data
- construct economically meaningful price series
- compute standardized return metrics
- provide basic liquidity information
- ensure reproducibility and consistency across assets

---

## Design Principles

### 1. Raw Data Immutability

Raw datasets are never modified.

All transformations are applied in this layer, ensuring:

- traceability
- reproducibility
- auditability

---

### 2. Point-in-Time Correctness

All computations are strictly **forward-looking safe**:

- no use of future information
- no lookahead bias
- correct temporal alignment

---

### 3. Total Return Representation

All return calculations are based on **total return prices**, incorporating:

- dividends
- capital gains

This ensures that:

- returns reflect actual investor experience
- assets are comparable across classes

---

### 4. Deterministic Transformations

Given the same raw input, the processed output is:

- deterministic
- reproducible
- stable across runs

---

### 5. Asset-Level Independence

Each asset is processed independently:

- one dataset per asset
- no cross-asset dependency at this stage

This enables:

- scalability
- parallelization
- modularity

---

## Data Structure

Each processed dataset is stored as:


`data/processed/{asset}.parquet`


### Properties

- Datetime index
- One row per timestamp
- Standardized column schema across all assets

---

## Core Components

### 1. Data Normalization

Raw vendor data is standardized:

- consistent column naming
- datetime index enforcement
- chronological ordering
- duplicate timestamp removal

---

### 2. Corporate Actions Adjustment

A **total return price series** is constructed:

- distributions = dividends + capital gains
- backward adjustment factors
- cumulative adjustment factor
- adjusted close (`adj_close`)

This produces a price series that is:

- continuous across distributions
- economically meaningful
- suitable for return computation

---

### 3. Return Computation

Logarithmic returns are computed using adjusted prices:

- daily returns (`log_ret`)
- multi-horizon returns:
  - 5 (weekly)
  - 21 (monthly)
  - 63 (quarterly)
  - 126 (semiannual)
  - 252 (annual)

These returns serve as the foundation for:

- volatility modeling
- regime detection
- risk analysis

---

### 4. Liquidity Features

Basic liquidity proxies are computed:

- dollar volume (`Close × Volume`)
- rolling averages:
  - 21-day
  - 63-day

These features support:

- liquidity filtering
- diagnostics
- capacity analysis

---

### 5. Schema Standardization

All datasets share:

- identical columns
- consistent column order
- aligned naming conventions

This is critical for:

- cross-asset analysis
- panel construction
- feature pipelines

---

## Output Dataset

Each asset dataset includes:

### Market Data

- Open, High, Low, Close, Volume
- vendor_adj_close

### Corporate Actions

- Dividends
- Capital Gains
- Stock Splits

### Adjusted Series

- distribution
- dist_factor
- cum_adj_factor
- adj_close

### Returns

- log_ret
- log_ret_{horizons}

### Liquidity

- dollar_volume
- rolling liquidity metrics

---

## Role in the System

The Processed Data Layer is the **bridge between raw data and research**.

It provides:

- a clean and consistent dataset
- a reliable base for feature engineering
- a standardized interface for downstream layers

---

## What This Layer Does NOT Do

- cross-asset alignment
- missing data imputation across assets
- feature normalization
- regime classification

These responsibilities belong to later stages of the system.