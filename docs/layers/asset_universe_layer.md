# Asset Universe Layer

## Overview

The Asset Universe Layer defines the **set of assets available for research and data processing**.

It acts as the **entry point of the entire system**, determining:

- which assets are downloaded
- which assets are processed
- which assets are included in research workflows

---

## Responsibilities

The Asset Universe Layer is responsible for:

- Defining the research universe
- Providing asset metadata
- Standardizing asset identification across the system

---

## Core Concept

An **asset** is not just a ticker.

It is a structured entity that includes:

- internal symbol
- external data source identifier
- asset type
- market classification
- optional metadata

---

## Asset Abstraction

Each asset must be uniquely identifiable through:

- `symbol` → internal identifier used across the system
- `external ticker` → identifier used by data providers

---

## Metadata

Assets may include metadata such as:

- asset type (equity, ETF, crypto, bond, commodity)
- market (US, Global, etc.)
- sector or category
- currency

This metadata enables:

- filtering
- grouping
- cross-asset analysis
- portfolio construction logic

---

## Output Contract

The layer provides:

- a list of asset objects
- consistent asset identifiers across all layers

---

## Position in Architecture

```
Asset Universe Layer
↓
Raw Data Layer
↓
Processed Data Layer
↓
Feature Layer
```


---

## Design Principles

### Consistency

All layers use the same asset identifiers.

### Extensibility

New assets can be added without changing downstream logic.

### Abstraction

The system never depends directly on external tickers.

---

## What This Layer Does NOT Do

The Asset Universe Layer does NOT:

- download data
- compute features
- perform transformations

It only defines **what assets exist in the system**.

---

## Role in Research

The universe defines the **scope of analysis**.

Changing the universe directly impacts:

- cross-asset studies
- regime detection
- allocation strategies

---

## Future Extensions

- dynamic universes (time-varying)
- region-based universes
- liquidity-filtered universes
- strategy-specific universes