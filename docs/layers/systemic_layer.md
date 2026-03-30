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
asset-level features → systemic features
```

Instead of analyzing each asset independently, we compute statistics **across assets at each point in time**.

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

## Output

The systemic layer produces a dataset:

### `df_systemic`

- **index**: datetime  
- **columns**: systemic features  

Example:


- mean_return
- dispersion_return
- breadth_momentum
- correlation_return
- ...

This dataset represents the **state of the market at each point in time**.

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

After transformations:

- remaining NaNs are removed (`dropna`)
- final dataset contains no missing values

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