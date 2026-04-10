# Regime Layer

## Overview

The **Regime Layer** transforms systemic market features into **interpretable market regimes**.

It operates on top of the **Systemic Layer** and produces a structured representation of market states that can be used for:

* allocation decisions
* risk management
* strategy conditioning
* backtesting

This layer is designed as a **model abstraction**, not an experiment engine.

---

## 🧠 Core Idea

The Regime Layer maps:

Systemic Features → Regime Probabilities → Regime Representation

It shifts the system from:

> descriptive analytics → decision-oriented state modeling

---

## 🧱 Responsibilities

The Regime Layer is responsible for:

### 1. Regime Modeling

* Transform systemic features into:

  * regime probabilities
  * regime scores

* Support multiple model types:

  * rule-based (current)
  * clustering (future)
  * HMM (future)
  * ML classifiers (future)

---

### 2. Regime Representation

Produce a structured output including:

* discrete regime labels
* probabilistic representation
* confidence metrics
* uncertainty measures

---

### 3. Abstraction & Extensibility

* Models must share a common interface
* Output schema must be consistent across models
* Must support plugging new models without changing downstream layers

---

## 📊 Output Schema

The Regime Layer outputs a time-indexed dataset:

| column        | description              |
| ------------- | ------------------------ |
| regime_prob_* | probability per regime   |
| label         | dominant regime (argmax) |
| confidence    | max probability          |
| entropy       | uncertainty measure      |

---

## 🧠 Design Principles

### 1. Model ≠ Research

The Regime Layer:

* DOES produce predictions
* DOES NOT optimize configurations

---

### 2. Probabilistic First

Even when using rule-based logic:

* output must be probabilistic
* labels are derived, not primary

---

### 3. Deterministic & Reproducible

Given:

* systemic dataset
* config

The output must be:

* deterministic
* reproducible

---

### 4. Config-Driven

All behavior must be defined through configuration:

* regimes
* rules
* thresholds
* model parameters

---

## 🔄 Position in the Pipeline

Processed Data → Feature Layer → Panel → Systemic Layer → **Regime Layer** → Allocation / Backtesting

---

## 🚫 Out of Scope

The Regime Layer does NOT handle:

* hyperparameter optimization
* search strategies (grid, random, Bayesian)
* experiment tracking

These belong to the **Research Layer**.

---

## 🎯 Role in the System

The Regime Layer acts as a:

> **State Modeling Engine**

It converts market structure into a form that downstream systems can act upon.

---

## 🧠 Key Insight

The value of the Regime Layer lies in:

* how well it captures **market state transitions**
* how stable and interpretable those states are
* how useful they are for downstream decisions

Not in how it is optimized.
