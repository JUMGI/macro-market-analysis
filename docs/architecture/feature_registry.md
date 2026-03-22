# Feature Registry

## Overview

The Feature Registry is the central component that defines, organizes, and exposes all available features in the system.

It acts as a metadata and orchestration layer that allows the system to dynamically discover, access, and compute features across different asset classes and feature families.

---

## Responsibilities

- Register feature families (e.g. momentum, volatility)
- Store feature specifications (`FeatureSpec`)
- Expose feature computation logic (`compute_fn`)
- Enable dynamic feature discovery
- Provide a structured and extensible feature system

---

## Key Concepts

### Feature Family

A feature family is a logical grouping of related features.

Examples:

- momentum
- volatility
- liquidity (future)
- microstructure (future)

Each family contains multiple features and their computation logic.

---

### FeatureSpec

A `FeatureSpec` represents a single feature definition.

It typically includes:

- `name`: feature identifier
- `family`: feature family
- `compute_fn`: function that computes the feature from raw data
- `metadata` (optional): description, parameters, etc.

Example:

FeatureSpec(
    name="MOM_63",
    family="momentum",
    compute_fn=compute_MOM_63,
)

Registry Structure
---
The registry is structured as:

family → feature_name → FeatureSpec

Example:

registry["momentum"]["MOM_63"]
registry["volatility"]["VOL_252"]



Initialization
---

The registry is initialized from a base path that contains feature definitions and/or configurations.

During initialization:

- feature modules are discovered

- feature specs are registered

- compute functions are linked to each feature

Example:

from quant_research.features.registry import create_registry

registry = create_registry(base_path)



Usage
---

- Retrieve a Feature

spec = registry.get(family="momentum", feature="MOM_63")

- Compute a Feature

df_feature = spec.compute_fn(df_raw)

- Example Workflow

registry = create_registry(base_path)

spec = registry.get("momentum", "MOM_63")

df_feature = spec.compute_fn(df_raw)

---

Design Principles

1. Extensibility

- New features can be added without modifying core logic.

2. Decoupling

- Feature logic is separated from data loading

- Registry does not depend on storage format

3. Discoverability

- Features can be queried dynamically from the registry.

4. Composability

- Features can be combined, reused, and extended across families and assets.

5. Deterministic Computation

- Given the same input data, feature computation must be deterministic.


## Registry vs Other Components
---

| Component                     | Responsibility                      |
|------------------------------|-------------------------------------|
| Feature Registry             | defines and organizes features      |
| Feature Loader               | reads feature data from disk        |
| Panel Builder                | aggregates data across assets       |
| Cross-Sectional Transformer  | transforms panel data               |

Important Notes

- The registry does NOT store data

- The registry does NOT perform I/O operations

- The registry does NOT align or merge assets

- It only defines and exposes feature logic

---
Future Extensions:

- Feature versioning

- Feature dependency graph

- Auto-validation of compute functions

- Feature metadata enrichment

- Integration with experiment tracking systems


Example Directory Structure
---

```
src/quant_research/features/
├── registry/
│   ├── asset_feature_registry.py
│   ├── feature_spec.py
│   └── registry_factory.py
│
├── asset/
│   ├── momentum/
│   │   └── momentum_features.py
│   └── volatility/
│       └── volatility_features.py
```

Final Insight
---

The Feature Registry is the source of truth for feature definitions in the system.

It allows the rest of the architecture to remain:

- modular  
- scalable  
- fully extensible  