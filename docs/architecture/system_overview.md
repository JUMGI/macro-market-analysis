# System Overview

## Objective

This project implements a structured quantitative research framework for:

- Asset allocation
- Regime detection
- Market structure analysis

The system is designed with strict layer separation to ensure:

- Research clarity
- Reproducibility
- Production migration capability
- Avoidance of logical leakage between components

---

## Layered Architecture

The framework follows a multi-layer design:

### 1. Data Layer

Responsibilities:
- Data ingestion
- Cleaning
- Alignment
- Return construction

Outputs:
- Clean price series
- Log returns
- Standardized panel format

---

### 2. Asset Characterization Layer

Purpose:
Describe structural statistical properties of each asset.

Includes:
- Momentum Family
- Volatility Family
- Cross-sectional dispersion (future)
- Derived composite metrics (future)

This layer only contains continuous features.
No regime classification.
No allocation logic.

---

### 3. Regime Detection Layer

Purpose:
Combine asset features to infer market states.

Examples:
- High momentum + low volatility
- High volatility transition states
- Structural stress regimes

Outputs:
- Continuous regime scores
- Optional regime labels

---

### 4. Allocation Layer

Purpose:
Translate regime and asset signals into portfolio weights.

Examples:
- Signal-weighted allocation
- Volatility scaling
- Optimization-based allocation

---

### 5. Evaluation Layer

Purpose:
Evaluate strategy performance.

Includes:
- Sharpe Ratio
- Rolling Sharpe
- Drawdown
- Conditional performance by regime

---

## Design Philosophy

- Primitive features first.
- Derived metrics later.
- Strict separation of responsibilities.
- No premature optimization.
