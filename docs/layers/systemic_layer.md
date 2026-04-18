# Systemic Layer

## Overview

The **Systemic Layer** is responsible for transforming asset-level features into **cross-asset representations of the market state**.

While previous layers focus on individual assets (price, returns, features), the systemic layer shifts the perspective to the **market as a system**, capturing aggregate behavior across assets.

This layer is the foundation for:

- regime detection
- macro state analysis
- cross-asset signals
- systematic allocation models

---

## Inputs

The systemic layer operates on a **feature panel** built in the Panel Layer.

### Panel Structure

- **index**: datetime
- **columns**: MultiIndex (feature, asset)

Example:

```
(MOM_63_Z, BTC) (MOM_63_Z, SPY) (VOL_63_Z, BTC) ...
```

### Requirements

The input panel must be:

- cross-asset aligned (union or intersection)
- validated (schema + consistency)
- reproducible

---

## Core Idea

The systemic layer applies **cross-sectional operators** to transform:

```
asset-level features (panel) → systemic feature instances
```

Instead of analyzing each asset independently, we compute statistics **across assets at each point in time**.

Additionally, systemic features can form a **directed acyclic graph (DAG)**:

- some features depend on raw panel features
- others depend on previously computed systemic features

Example:

`mean(MOM_63) → zscore(mean(MOM_63))`


This enables composability and layered transformations.

---

## Systemic Feature Families

The following families define the initial systemic representation:

### 1. Mean (Market Direction)

Cross-asset average of a feature.

$$
\mu_t = \frac{1}{N} \sum_{i=1}^{N} x_{i,t}
$$

Captures the **aggregate direction** of the market.

---

### 2. Dispersion (Disagreement / Risk)

Cross-asset standard deviation.

$$
\sigma_t = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_{i,t} - \mu_t)^2}
$$

Measures **heterogeneity across assets**.

---

### 3. Breadth (Participation)

Fraction of assets satisfying a condition (e.g. positive momentum).

$$
\text{Breadth}_t = \frac{1}{N} \sum_{i=1}^{N} \mathbf{1}(x_{i,t} > 0)
$$

Captures **how widespread a signal is**.

---

### 4. Correlation (Systemic Coupling)

Average pairwise correlation across assets.

$$
\rho_t = \text{mean}(\text{corr}(X_t))
$$

Measures **how synchronized the market is**.

---

## Feature Definition

Systemic features are defined via configuration and expanded into **feature instances**.

Each feature instance contains:

- name
- type (aggregator)
- inputs
- params

This enables:

- parameter sweeps (via config expansion)
- reproducible experiments
- consistent feature generation

---


## Output

The systemic layer produces a **dataset bundle** composed of:

### 1. `systemic.parquet`

- cross-asset aggregated features
- **index**: datetime
- **columns**: systemic feature names

### 2. `systemic_z.parquet`

- standardized version of the dataset (z-score applied column-wise)

$$
Z = \frac{X - \mu}{\sigma}
$$

- computed **after final NaN handling**

---

### 3. `metadata.json`

The metadata is the **single source of truth** describing the dataset.

It includes:

#### Dataset-level metadata

- `name`
- `dataset_hash`
- `panel_hash`
- `config_hash`
- `n_rows`
- `n_features`

#### Feature-level metadata (enriched)

Each feature contains:

- `measure` → what is being measured (e.g. momentum, volatility)
- `operator` → cross-sectional operator (mean, std, etc.)
- `transform` → optional transformation (e.g. zscore)
- `domain` → semantic grouping
- `inputs` → dependencies (panel features or upstream systemic features)
- `params` → configuration parameters

This allows:

- full traceability
- feature grouping
- downstream research (feature selection, regime modeling)

---

## Data Treatment

The systemic layer includes explicit handling of missing data:

### 1. Warmup Removal

Initial periods with insufficient lookback are removed.

- based on selected features
- ensures all features are valid

---

### 2. Calendar Handling

Cross-asset calendars are unified:

- `ffill` → preserve full timeline (recommended for systemic analysis)
- `drop` → restrict to common trading days

---

### 3. Final NaN Policy

Final NaN handling is applied **before export**, based on configuration:

- if `dropna` → rows with NaNs are removed
- otherwise → NaNs may remain

This policy directly impacts:

- `systemic.parquet`
- `systemic_z.parquet`

---

## Design Principles

The systemic layer follows these principles:

- **Config-driven**  
  All behavior (features, assets, NaN handling) is defined via configuration

- **Deterministic**  
  Same inputs → same outputs

- **Reproducible**  
  Dataset can be reconstructed from config + pipeline

- **Decoupled**  
  Independent from panel construction and feature engineering

- **Transparent**  
  All transformations are explicit and auditable

---

## Reproducibility & Hashing

Each systemic dataset is uniquely identified using hashes:

- **dataset_hash** → hash of `systemic.parquet`
- **panel_hash** → hash of input panel
- **config_hash** → hash of full configuration

This enables:

- exact reproducibility
- dataset versioning
- integrity checks across pipeline stages

Any change in:

- input data
- configuration
- feature definitions

will result in a different dataset hash.

---

## Role in the Pipeline

The systemic layer sits between feature engineering and regime modeling:

```
RAW → PROCESSED → FEATURES → PANEL → SYSTEMIC → REGIMES → ALPHA
```

It acts as a **bridge** between:

- micro (asset-level features)
- macro (market state)

---

## Interpretation

Systemic features allow us to observe:

- market direction (mean)
- disagreement (dispersion)
- participation (breadth)
- synchronization (correlation)

Together, they form a **low-dimensional representation of market dynamics**.

---

## Future Extensions

The systemic layer can be extended with:

- additional feature families
- feature selection techniques
- dimensionality reduction (PCA, autoencoders)
- machine learning representations
- regime classification models

### Integration with Exogenous Data

The systemic layer can be complemented with **exogenous variables**, such as:

- macroeconomic indicators
- sentiment measures
- market positioning data

These variables are not part of the systemic layer itself, but can be integrated at later stages (e.g. regime detection) to enrich the representation of market conditions.

This separation ensures a clear distinction between:

- endogenous market behavior (systemic layer)
- external drivers (exogenous layer)

---

## Summary

The systemic layer transforms a collection of asset-level signals into a **coherent representation of the market as a system**, enabling higher-level modeling such as regime detection and allocation strategies.

## Integration with Feature Validation

The systemic layer is designed to integrate with the Feature Validation layer.

- metadata provides feature-level descriptors
- validation computes quality metrics (stability, redundancy, etc.)

This enables:

- systematic feature selection
- research-driven filtering
- robust downstream modeling