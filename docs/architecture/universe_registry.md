# Universe Registry

## Overview

The universe registry implements the **Asset Universe Layer**.

It defines the set of assets used across:

- raw data ingestion
- feature engineering
- research workflows

---

## Location


`src/quant_research/data/registry/universe_registry.py`


---

## Asset Object

Assets are represented using a structured dataclass.

### Fields

- `symbol`: internal identifier
- `asset_type`: classification (equity, etf, crypto, etc.)
- `market`: geographical or logical market
- `sector`: optional classification
- `group`: higher-level grouping
- `currency`: default USD
- `yfinance_ticker`: optional external ticker override

---

## Example

```python
Asset(
    symbol="BTC",
    asset_type="crypto",
    market="Global",
    group="crypto",
    yfinance_ticker="BTC-USD"
)
```
## Universe Definition

The universe is defined as a list:
```python
ASSET_UNIVERSE = [
    Asset("SPY", "etf", "US", group="equity"),
    Asset("QQQ", "etf", "US", group="equity"),
    Asset("BTC", "crypto", "Global", group="crypto", yfinance_ticker="BTC-USD"),
]
```
---

## Helper Functions

The registry exposes utility functions:

`get_symbols()`

Returns internal asset symbols.

`get_tickers()`

Returns external data provider tickers.

`get_assets_by_type()`

Filter assets by type.

`get_groups_by_type()`

Group assets by asset type.

---
## Design Decisions

### Asset Abstraction

All operations use structured Asset objects instead of raw strings.

### Internal vs External Identifiers
- `symbol` → used internally
- `ticker` → used for data providers

This decouples the system from external APIs.

### Centralized Definition

The universe is defined in a single location, ensuring consistency.

### Integration

The registry is used by:

- raw data pipeline → iteration over assets
- feature pipeline → asset-level processing
- research notebooks → universe selection

### Limitations (Current)
- static universe (no time dimension)
- no liquidity filters
- no dynamic inclusion/exclusion

### Future Extensions
- dynamic universes
- factor-based selection
- region-specific subsets
- universe versioning