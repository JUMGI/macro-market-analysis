# Volatility Family

**Layer:** Asset Characterization  
**Status:** Research Stable  
**Type:** Continuous Features Only  

---

# 1. Objective

Construct a **multi-horizon volatility characterization layer** capturing:

- Volatility level
- Volatility dynamics
- Volatility structure across horizons
- Volatility regime positioning
- Volatility instability

The output is a **multi-index DataFrame**:

**Columns**

- level 0 → feature
- level 1 → asset

**Rows**

- datetime index

---

# 2. Input Assumptions

- Clean adjusted close prices
- No missing timestamps inside trading calendar
- Log returns used for volatility computation
- Annualization factor applied where required
- All calculations performed per asset independently

Let:

$$
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
$$

where \(P_t\) denotes the adjusted close price.

---

# 3. Feature Blocks

## 3.1 Volatility Level

Realized volatility is computed as the rolling standard deviation of log returns.

$$
VOL_h = \sqrt{252} \cdot \sigma_h(r_t)
$$

where

$$
\sigma_h(r_t) = \sqrt{\frac{1}{h} \sum_{i=1}^{h}(r_{t-i}-\bar{r})^2}
$$

**Horizons**

- 21
- 63
- 126
- 252

These produce the following features:

VOL_21
VOL_63
VOL_126
VOL_252


**Purpose**

Capture short, medium and long-term volatility environments.

---

## 3.2 Volatility Dynamics

Volatility dynamics capture the **speed and curvature of volatility changes**.

### Velocity

First difference of volatility:

$$
VOL_{h,CHG}(t) = VOL_h(t) - VOL_h(t-1)
$$

### Acceleration

Second difference of volatility:

$$
VOL_{h,ACC}(t) = VOL_{h,CHG}(t) - VOL_{h,CHG}(t-1)
$$

### Smoothed variants

Smoothed versions are used to reduce noise:
VOL_h_CHG_S
VOL_h_ACC_S


**Purpose**

Detect:

- volatility shocks
- volatility expansion
- volatility stabilization phases

---

## 3.3 Volatility Structure

The term structure of volatility is captured through **spreads and ratios between horizons**.

### Volatility spreads

$$
VOL\_TERM_{21,63} = VOL_{21} - VOL_{63}
$$

$$
VOL\_TERM_{21,126} = VOL_{21} - VOL_{126}
$$

$$
VOL\_TERM_{21,252} = VOL_{21} - VOL_{252}
$$

Features:
VOL_TERM_21_63
VOL_TERM_21_126
VOL_TERM_21_252


### Volatility ratios

$$
VOL\_RATIO_{21,63} = \frac{VOL_{21}}{VOL_{63}} - 1
$$

$$
VOL\_RATIO_{21,126} = \frac{VOL_{21}}{VOL_{126}} - 1
$$

$$
VOL\_RATIO_{21,252} = \frac{VOL_{21}}{VOL_{252}} - 1
$$

Features:
VOL_RATIO_21_63
VOL_RATIO_21_126
VOL_RATIO_21_252


**Purpose**

Capture short-term volatility dislocations relative to longer-term volatility regimes.

---

## 3.4 Volatility of Volatility

Volatility of volatility measures the **instability of the volatility process itself**.

$$
VOV_{21,63} = \sigma_{63}(VOL_{21})
$$

Feature:
VOV_21_63


**Purpose**

Identify turbulent periods where volatility itself becomes unstable.

High values indicate:

- regime transitions
- market stress
- structural volatility shifts

---

## 3.5 Volatility Regime Indicators

Volatility regimes are characterized using standardized measures relative to historical distributions.

### Z-score normalization

Short-term regime:

$$
VOL_{21,Z} =
\frac{VOL_{21} - \mu_{252}(VOL_{21})}{\sigma_{252}(VOL_{21})}
$$

Long-term regime:

$$
VOL_{252,Z} =
\frac{VOL_{252} - \mu_{252}(VOL_{252})}{\sigma_{252}(VOL_{252})}
$$

Features:
VOL_21_Z
VOL_252_Z

### Percentile rank

Short-term percentile positioning:

$$
VOL_{21,PCTL} =
\text{PercentileRank}_{252}(VOL_{21})
$$

Feature:
VOL_21_PCTL


### Volatility expansion indicator

Short vs medium horizon expansion:

$$
VOL_{21,EXP63} =
\frac{VOL_{21}}{VOL_{63}} - 1
$$

Feature:
VOL_21_63_EXP


**Purpose**

Normalize volatility relative to historical distributions and detect structural risk regimes.

---

# 4. Design Principles

- No discretization inside this layer
- All features remain continuous
- No regime labeling performed here
- No allocation logic embedded
- Feature definitions remain asset-specific

The architecture follows a strict **separation of concerns** principle.

---

# 5. Known Limitations

- Rolling windows introduce warm-up NaNs
- Long horizons reduce effective sample size
- Extreme events may dominate rolling statistics
- Volatility clustering can produce persistent high regimes

---

# 6. Downstream Usage

The Volatility Family feeds the following layers:

- **Correlation Structure Layer**
- **Cross-Asset Systemic Risk Analysis**
- **Regime Detection Layer**
- **Portfolio Risk Controls**

These features are designed to integrate with the **global research feature panel** and support higher-level market structure analysis.
