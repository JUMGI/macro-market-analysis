# Feature Validation Layer - Implementation

## Overview

This document describes the implementation details of the Feature Validation Layer.

The layer is designed to be:

- modular
- config-driven
- extensible
- reproducible

---

## Directory Structure

```
feature_validation/
    metrics/
            stability.py
            autocorr.py
            missing.py
            redundancy.py
            registry.py

profiles/
    systemic.py

engine/
    validator.py

models/
    metadata.py

store/
    store.py

configs/
    systemic_v1.json
    loader.py
    validator.py

utils/
    hash.py 
    
```


---

## Core Components

### 1. Metrics

Each metric is implemented as a standalone function.

Signature:

```python
def metric(series, full_df=None, **params):
    pass
```

Examples:

- compute_stability
- compute_autocorr
- compute_missing
- compute_redundancy

---

## 2. Metric Registry

Maps metric names to implementations.
```python
METRIC_REGISTRY = {
    "stability": compute_stability,
    "autocorr": compute_autocorr,
    "missing": compute_missing,
    "redundancy": compute_redundancy,
}
```
---

## 3. Profiles

Profiles define how metrics are applied.

Current profile:

- SystemicValidationProfile

Responsibilities:

- read config
- iterate over enabled metrics
- execute metrics dynamically

---

## 4. Validator

The FeatureValidator orchestrates:

- iteration over features
- execution of profile
- aggregation of results
- creation of metadata artifact

---

## 5. FeatureMetadata

Represents the output artifact.

Fields:

- dataset_id
- dataset_hash
- fv_hash
- metrics
- config
- created_at

---

## 6. Hashing

Feature validation runs are identified by:

`fv_hash = hash(dataset_hash + config)`

This ensures:

- deterministic outputs
- caching capability
- experiment tracking

---
## 7. Config System

Validation is controlled via JSON config files.

Example:
```python
{
    "metrics": {
        "stability": {
            "enabled": true,
            "params": { "window": 63 }
        }
    }
}
```

---
## 8. Config Validation

Config is validated using introspection:

- metric exists in registry
- params match function signature
- required params are present

---
## 9. Store

Artifacts are stored as:

data/feature_validation/{dataset_id}/{fv_hash}.json

### Execution Flow
```
Load dataset
    ↓
Load config
    ↓
Validate config
    ↓
Instantiate profile
    ↓
Run FeatureValidator
    ↓
Compute fv_hash
    ↓
 Save FeatureMetadata
```
---
### Example Usage

```python
df, sys_meta = load_systemic_dataset("baseline_v2")

config = load_validation_config("systemic_v1")

profile = SystemicValidationProfile(config=config)

validator = FeatureValidator(
    profile=profile,
    dataset_id=sys_meta["name"],
    dataset_hash=sys_meta["dataset_hash"],
    config=config
)

fv_metadata = validator.validate(df)

FeatureValidationStore.save(fv_metadata)
```
---
### Design Decisions
Separation of IO
- No file reading inside validator or profile
- Data loading handled externally

---
### Config-Driven Execution
- No hardcoded metrics
- Fully controlled by config

---
### Plugin-Based Metrics
- New metrics require no profile changes
- Only registry update

---
### Deterministic Artifacts
- Same input → same `fv_hash` → same output

---
### Future Extensions
- Type validation for config params
- Feature scoring functions
- Integration with research pipeline
- Alpha-specific validation profiles
- Feature clustering and grouping

---
### Summary

The implementation provides:

- modular architecture
- extensible metric system
- reproducible validation runs
- strong config validation

This layer is the foundation for systematic feature selection in the research pipeline.