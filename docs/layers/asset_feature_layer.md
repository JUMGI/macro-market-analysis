# Asset Feature Layer

## Overview

The Asset Feature Layer is responsible for transforming processed market data into 
continuous, asset-level statistical descriptors.

These features represent the fundamental building blocks for:

- cross-asset analysis
- regime detection
- allocation models

This layer is strictly **non-predictive** and **non-decisional**.

---

## Responsibilities

Allowed:

- Rolling statistical computations
- Transformations of price / returns / volume
- Feature normalization (z-score, percentile, stability)
- Multi-horizon descriptors (e.g. momentum, volatility)
- Structural metrics (alignment, term structure)

Not allowed:

- Regime labeling
- Signal generation
- Portfolio allocation
- Performance evaluation
- Forward-looking transformations (no lookahead bias)

---

## Architecture

The layer is composed of four core components:

### 1. Compute Modules

Location:
src/quant_research/features/asset/{family}/compute.py

Each family defines:

- compute_features(df) → DataFrame
- get_feature_columns() → List[str]

These define:

- feature logic
- feature schema

---

### 2. Feature Schema

Each feature family explicitly defines its output columns via:

get_feature_columns()

This ensures:

- deterministic outputs
- schema validation
- reproducibility

---

### 3. Feature Registry

Location:
src/quant_research/features/registry/

The registry provides:

- a catalog of feature families
- access to compute functions
- metadata (inputs, outputs, frequency)

Key property:

The registry is **data-independent** and **fully declarative**.

---

### 4. Feature Loader

Location:
src/quant_research/features/loaders/

Responsible for:

- loading stored features from disk
- filtering by asset, date, or feature subset

Storage format:

data/features/asset/{family}/{asset}.parquet

---

## Data Model

Each feature file follows:

- index: datetime (asset-specific)
- columns: feature names
- no cross-asset alignment at this stage

Example:

SPY:
2000 → present

BTC:
2014 → present

---

## Design Principles

- Deterministic: same input → same output
- Stateless: no hidden dependencies
- Modular: each family is independent
- Scalable: new families plug into registry
- Reproducible: schema is explicitly defined

---

## Output Role in System

The output of this layer feeds:

→ Panel Builder  
→ Regime Detection Layer  
→ Allocation Models  

This layer defines the **feature space of the system**.