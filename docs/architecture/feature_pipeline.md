# Feature Pipeline

## Overview

The Feature Pipeline orchestrates the full lifecycle of feature generation:

raw data → feature computation → schema validation → storage

It is the **single source of truth** for feature production.

---

## Pipeline Flow

For each asset and feature family:

1. Load processed data
2. Compute features using registry
3. Validate schema
4. Save features to disk
5. (Optional) run value validation

---

## Input

- Processed data:
  data/processed/{asset}.parquet

- Feature families:
  defined in FeatureRegistry

---

## Output

Stored features:

`data/features/asset/{family}/{asset}.parquet`

---

## API

```python
pipeline.run(
    assets: List[str],
    families: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    validate: bool = False,
    overwrite: bool = True
)
python```

---

## Core Components

FeaturePipeline

**Location**
`src/quant_research/features/pipeline/feature_pipeline.py`

Responsibilities:

- orchestration
- schema validation
- file management

---

## Feature Registry Integration

The pipeline uses the registry to:

- resolve compute functions
- enforce feature schemas

```python
spec = registry.get_by_family(family)[0]
df = spec.compute_fn(df_raw)```


---

## Schema Validation

Before saving:
```python
expected = set(spec.output_columns)
actual = set(df.columns)
python```

The pipeline enforces:

`expected == actual`

This prevents:

- missing features
- unexpected columns
- silent bugs

---

## Storage

Features are stored per asset:

`data/features/asset/{family}/{asset}.parquet`

This ensures:

- independence across assets
- flexibility in time ranges
- compatibility with panel builder

---

## Design Principles

- Idempotent: safe to re-run
- Deterministic: reproducible outputs
- Modular: decoupled from specific feature logic
- Registry-driven: no hardcoding of families
- Validated: schema enforcement prevents drift

---

## Role in Research Workflow

The pipeline separates:

**Feature generation (production layer)**
vs
**Feature analysis (research layer)**

This allows notebooks to remain:

- lightweight
- reproducible
- focused on analysis

---

## System Integration

The pipeline feeds:

→ Feature Loader
→ Panel Builder

and ultimately:

→ Regime Detection
→ Allocation Models




