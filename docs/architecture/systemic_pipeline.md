# Systemic Pipeline Architecture

## Overview

The **Systemic Pipeline** is responsible for transforming an asset-level feature panel into **cross-asset systemic indicators** that describe the global state of the market.

It sits above the asset feature layer and below the regime layer.

---

## Position in Architecture

Asset Features (MOM, VOL, RET, etc.)
        ↓
Panel Builder (estructura + raw panel)
        ↓
Panel Preparer (cleaning + alignment + NaNs)
        ↓
Systemic Pipeline (cross-asset aggregation)
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
- columns: MultiIndex [asset, feature]


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

The pipeline produces:

### Systemic DataFrame
index: time
columns:
    mean_mom
    mean_vol
    dispersion_mom
    dispersion_ret
    breadth_mom
    corr_ret
    corr_mom
    mean_mom_z

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
## Output Contract

Each run produces:

- `systemic_features.parque`t
- `systemic_features_z.parquet`
- `metadata.json`

---
## Metadata Design

Metadata includes:

### Identity
- run name
- timestamp
- dataset hash
- config hash

### Data summary
shape
- columns
- assets
- date range

### Systemic summary
- feature list
- feature count

### Audit
- nan checks
- extreme values
- validation status

---
## Pipeline Guarantees
- No NaNs (post-cleaning stage)
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

---
## Summary

The Systemic Pipeline converts asset-level signals into a compact representation of market state, enabling:

- regime detection
- risk modeling
- strategy conditioning