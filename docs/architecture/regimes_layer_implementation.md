# Regime Layer — Implementation

## Overview

The **Regime Layer** is responsible for transforming a **systemic dataset** into a **time series of market regimes**, represented both:

* **discretely** (labels)
* **probabilistically** (regime probabilities)

This layer is:

* fully **config-driven**
* **model-agnostic** (rule-based today, extensible to ML models)
* designed for **reproducibility and integration** with the Research Layer

---

## Core Responsibilities

The Regime Layer is strictly responsible for:

1. **Model execution**
2. **Regime representation (output)**
3. **Metadata generation**
4. **Input validation (planned)**
5. **Post-processing (planned)**

It explicitly does NOT handle:

* evaluation
* optimization
* experiment orchestration

---

## Architecture

```
systemic_df + systemic_metadata + config
        ↓
   validation              
        ↓
   model_registry
        ↓
   model.predict_proba()
        ↓
   processor_pipeline         
        ↓
   output_builder
        ↓
   regime_df
        ↓
   metadata_builder
        ↓
   metadata
```

---

## Folder Structure

```
regimes/
│
├── models/
│   ├── base.py
│   └── rule_based/
│       ├── model.py
│       ├── condition_evaluator.py
│       ├── rule_evaluator.py
│       └── scorer.py
│
├── outputs/
│   ├── builder.py
│   └── metrics.py
│
├── metadata/
│   └── builder.py
│
├── registry/
│   └── model_registry.py
│
├── processors/
│ ├── base.py
│ ├── pipeline.py
│ ├── smoothing.py
│ ├── thresholding.py
│ ├── persistence.py
│ ├── hysteresis.py
│ └── ensemble.py
│
├── validation/
│ └── feature_validator.py
│
└── utils/
    └── math.py
```

---

## Models

### Base Model

Defines the interface for all regime models:

```python
predict_proba(X: pd.DataFrame) -> pd.DataFrame
```

Output:

* index: datetime
* columns: regime names
* values: probabilities

---

### Rule-Based Model (current implementation)

* Uses structured declarative rules
* Evaluates conditions → rules → regime scores
* Converts scores → probabilities via softmax

Key components:

* `ConditionEvaluator`
* `RuleEvaluator`
* `RegimeScorer`

---

## Model Registry

The registry is responsible for constructing models from config.

### Design

* Maps `model.type` → constructor function
* Handles dependency injection (evaluators, scorer)

### Example

```python
model = create_model(config)
```

### Benefits

* decouples config from implementation
* enables plug-and-play models
* supports future extensions (HMM, clustering, ML)

---
## Processor Pipeline

### Purpose

Transforms **raw model probabilities** into more stable and usable regime signals.

The pipeline operates on **probability space**, enabling smooth transformations before final regime decisions are made.

---

## Soft vs Hard Processing

### Soft Processors

Operate on probabilities and preserve uncertainty.

Examples:

- rolling mean
- exponential smoothing
- ensemble smoothing

Output remains probabilistic.

---

### Hard Processors

Convert probabilities into discrete regimes.

Examples:

- persistence
- hysteresis
- thresholding (partial)

Output becomes deterministic (0/1 regimes).

---

## Implemented Processors

### Smoothing

- `RollingMeanSmoother`
- `ExponentialSmoother`

### Signal Filtering

- `ThresholdingProcessor`

### Regime Stabilization

- `PersistenceProcessor`
- `HysteresisProcessor`

### Signal Blending

- `EnsembleSmoother`

---

## Pipeline Execution

```python
pipeline = ProcessorPipeline.from_config(config["processors"])
probs = pipeline.apply(probs)
```
### Pipeline Principle
soft → soft → soft → hard → hard

### Key Design Principle
- Soft processors first → reduce noise, preserve information
- Hard processors last → enforce stability and decisions

Once a hard processor is applied, probabilistic information is no longer recoverable.

---
## Validation

### Feature Validator

Ensures that all features required by the regime configuration exist in the systemic dataset.

---

### Purpose

Prevent runtime errors caused by missing or misconfigured features.

---

### Example

```python
FeatureValidator().validate(config, systemic_metadata)
```
---
### Behavior
- extracts required features from the config
- compares them with available features in the systemic dataset
- raises a clear error if any feature is missing
---
### Design Principles
- validation is config-driven
- executed before model execution
- enforces fail-fast behavior
- guarantees consistency between config and data
---
### Output
- raises ValueError if validation fails
- otherwise allows pipeline execution to continue
---
## Output Builder

Transforms probabilities into a structured regime dataset.

### Output Schema

```
date | label | prob_bull | prob_bear | ...
```

Includes:

* discrete regime label (argmax)
* full probability distribution
* optional metrics (entropy, confidence)

---

## Metadata Builder

Generates metadata describing the regime run.

### Purpose

* reproducibility
* traceability
* data lineage

---

### Input

```python
build(regime_df, config, systemic_metadata)
```

---

### Output Structure

```json
{
  "name": "regime_v1",
  "created_at": "...",

  "model": {
    "type": "rule_based",
    "config_hash": "...",
    "n_regimes": 2,
    "regimes": ["bull", "bear"]
  },

  "features": {
    "used": [...],
    "missing": []
  },

  "systemic": {
    "name": "baseline_v2",
    "dataset_hash": "...",
    "config_hash": "...",
    "n_features": 34,
    "date_range": {
      "start": "...",
      "end": "..."
    }
  }
}
```

---

### Design Principles

* references systemic metadata (does not duplicate it)
* captures only necessary information
* enables full data lineage:

```
Regime → Systemic → Panel → Features → Processed
```

---


## What the Regime Layer Produces

Final output:

```python
{
    "regime_df": pd.DataFrame,
    "metadata": dict
}
```

---

## Design Principles

### 1. Separation of Concerns

* modeling (regimes)
* evaluation (research)
* optimization (research)

---

### 2. Config-Driven

* all behavior defined via config
* no hardcoded logic

---

### 3. Reproducibility

* config hash
* systemic dataset reference
* metadata lineage

---

### 4. Extensibility

* new models via registry
* new processors via pipeline

---

### 5. Minimalism

* only essential components included
* no premature abstraction

---

## What Comes Next

The Regime Layer integrates into the **Research Layer**, where:

* experiments are executed
* configurations are explored
* models are evaluated
* results are stored and analyzed

---

## Summary

The Regime Layer is a **modular, production-ready component** that:

* transforms systemic signals into regimes
* provides probabilistic and discrete outputs
* ensures reproducibility via metadata
* is ready for integration into a full research workflow

---
