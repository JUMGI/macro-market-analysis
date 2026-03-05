# Layer Definition & Responsibility Boundaries

This document defines strict rules to avoid cross-layer contamination.

---

## Data Layer

Allowed:
- Price adjustments
- Missing value handling
- Return computation
- Resampling

Not allowed:
- Feature engineering
- Signal generation

---

## Asset Characterization Layer

Allowed:
- Continuous statistical descriptors
- Rolling computations
- Structural measures (momentum, volatility)

Not allowed:
- Regime labeling
- Portfolio weights
- Strategy performance metrics

---

## Regime Detection Layer

Allowed:
- Combine asset features
- Build regime indicators
- Classification or clustering

Not allowed:
- Allocation sizing
- Strategy evaluation metrics

---

## Allocation Layer

Allowed:
- Portfolio weight construction
- Risk budgeting
- Signal weighting
- Constraint handling

Not allowed:
- Performance reporting beyond allocation outputs

---

## Evaluation Layer

Allowed:
- Sharpe
- Sortino
- Drawdowns
- Rolling diagnostics
- Conditional performance analysis

Not allowed:
- Feature creation
- Regime redefinition

---

## Architectural Principle

Each layer must be independently testable.
Each layer must receive inputs only from previous layers.
No backward logical dependencies are allowed.
