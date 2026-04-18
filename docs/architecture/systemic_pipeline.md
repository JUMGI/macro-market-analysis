# Systemic Pipeline Architecture

## Overview

The **Systemic Pipeline** is responsible for transforming an asset-level feature panel into **cross-asset systemic indicators** that describe the global state of the market.

It sits above the asset feature layer and below the regime layer.

---

## Position in Architecture

Asset Features (MOM, VOL, RET, etc.)
        ↓
Panel Builder (raw cross-asset panel)
        ↓
Panel Preparer (cleaning + alignment + NaNs)
        ↓
Systemic Pipeline (feature DAG + cross-asset aggregation)
        ↓
Regime Layer
        ↓
Strategy Layer


---

## Objective

The Systemic Pipeline aims to extract:

- Market trend (global momentum direction)
- Volatility regime (risk level)
- Dispersion (cross-asset disagreement)
- Breadth (market participation)
- Correlation structure (systemic risk / coupling)
- Optional transforms (smoothing / normalization)

---

## Input

The pipeline consumes:

### 1. Panel (asset-level features)

A multi-asset DataFrame:


- index: time
- columns: MultiIndex [feature, asset]


Example features:

- MOM_63_Z
- VOL_63_Z
- RET_1

---

### 2. Configuration

All systemic transformations are defined via config:

```python
CONFIG["systemic"]["features"]
```

Each entry defines:

- type (mean, dispersion, breadth, correlation, zscore)
- input features
- optional parameters (window, threshold)

These configurations are expanded into **feature instances**, where:

- each combination of parameters generates a concrete feature
- features become nodes in a computation graph (DAG)

This allows:

- parameter sweeps (e.g. multiple lookbacks)
- composability of transformations
- reproducible feature generation

---

## Systemic Feature Families
### 1. Trend / Momentum

Example:
```python 
mean_mom = mean(MOM_63 across assets)
```
Represents:
- global directional bias of market

### 2. Volatility Level

Example:
```python
mean_vol = mean(VOL_63_Z across assets)
```
Represents:
- global risk regime

### 3. Dispersion

Example:
```python
dispersion_mom = std(MOM_63_Z across assets)
```

Represents:
- disagreement between assets
- regime instability

### 4. Breadth
Example:
```python
breadth_mom = % assets where MOM_63_Z > threshold
```
Represents:
- participation in trend
- market conviction

### 5. Correlation Structure

Rolling cross-asset correlation:
```python
corr_ret = rolling_corr(RET_1, window=20)
```
Represents:

- systemic coupling
- crisis clustering behavior

### 6. Transforms

Optional post-processing:

- zscore normalization
- smoothing (future extension)
- regime scaling

Example:
```python
mean_mom_z = zscore(mean_mom, window=20)
```
---
## Output

The pipeline produces a **dataset bundle**:

### 1. `systemic.parquet`

- cross-asset systemic features
- **index**: datetime
- **columns**: feature names

---

### 2. `systemic_z.parquet`

- standardized version (z-score per feature)

$$
Z = \frac{X - \mu}{\sigma}
$$

- computed after final NaN handling

---

### 3. `metadata.json`

The metadata is the **single source of truth** for the dataset.

It includes:

#### Dataset-level

- name
- dataset_hash
- panel_hash
- config_hash
- n_rows
- n_features

#### Feature-level (enriched)

For each feature:

- measure
- operator
- transform
- domain
- inputs
- params

This enables:

- traceability
- feature grouping
- downstream research workflows

---
## Computation Model

Systemic features are computed as a **Directed Acyclic Graph (DAG)**:

- base features depend on panel inputs
- derived features depend on previously computed systemic features

Example:
`mean(MOM_63) → zscore(mean(MOM_63))`


This enables:

- composability
- reuse of intermediate features
- flexible feature pipelines
---

## Design Principles
### 1. Config-driven

All transformations are defined in config:
- no hardcoded features
- fully reproducible

### 2. Stateless computation

Systemic features are:

- deterministic
- derived from panel only
- independent of downstream regimes

### 3. Cross-asset aggregation

Systemic layer transforms:

- `asset space → market space`

### 4. Reproducibility

Each run is fully reproducible via:

- dataset_hash
- config_hash
- full config snapshot in metadata

---

## Hashing

Each dataset is uniquely identified by:

- dataset_hash → hash of systemic dataset
- panel_hash → hash of input panel
- config_hash → hash of configuration

This ensures:

- exact reproducibility
- version control of datasets
- consistency across pipeline stages
---

## Output Contract

Each run produces:

- `systemic.parquet`
- `systemic_z.parquet`
- `metadata.json`

---
## Metadata Design

Metadata includes:

### Dataset Identity

- name
- dataset_hash
- panel_hash
- config_hash

---

### Dataset Summary

- n_rows
- n_features

---

### Feature Metadata (enriched)

Each feature contains:

- measure
- operator
- transform
- domain
- inputs
- params

---

### Purpose

Metadata enables:

- reproducibility
- feature introspection
- integration with feature validation layer
- downstream research (selection, clustering, regimes)

---
## Pipeline Guarantees
- NaN handling is config-driven (may include dropna)
- Deterministic output
- Consistent feature ordering
- Fully reproducible results

---
## Future Extensions

Planned enhancements:

### 1. Multi-scale systemic features
- short / medium / long horizon aggregation
### 2. Regime-aware transforms
- dynamic normalization based on regime
### 3. Non-linear aggregators
- entropy-based dispersion
- PCA systemic factors
### 4. Graph-based correlation
- asset network structure
- clustering regimes
### 5. Feature validation integration
- quality-based feature filtering
- redundancy reduction
- stability-aware selection

---
## Summary

The Systemic Pipeline converts asset-level signals into a compact representation of market state, enabling:

- regime detection
- risk modeling
- strategy conditioning