# Volatility Family

**Layer:** Asset Characterization  
**Status:** Research Stable  
**Type:** Continuous Features Only  

---

# 1. Objective

Construct a **multi-horizon volatility characterization layer** capturing:

- Volatility level  
- Volatility dynamics (derivatives)  
- Volatility structure across horizons  
- Volatility regime positioning  
- Volatility instability  
- Volatility strength (composite signal)  

The output is a **single-index DataFrame per asset**.

**Columns**

- feature columns for that specific asset

**Rows**

- datetime index (aligned to the asset’s own trading calendar) 

---

# 2. Input Assumptions

- Clean adjusted close prices  
- No missing timestamps inside trading calendar  
- Log returns used for volatility computation  
- All calculations performed per asset independently  

Let:

$$
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
$$

---

# 3. Feature Blocks

---

## 3.1 Volatility Level

Realized volatility is computed as rolling standard deviation of log returns:

$$
VOL_h = \sigma_h(r_t)
$$

Where:

$$
\sigma_h(r_t) = \sqrt{\frac{1}{h} \sum_{i=1}^{h}(r_{t-i}-\bar{r})^2}
$$

**Horizons**

- 5  
- 21   
- 63    
- 126  
- 252  

**Features**

- VOL_5  
- VOL_21    
- VOL_63    
- VOL_126  
- VOL_252  

### Z-score normalization

$$
VOL_{h,Z} =
\frac{VOL_h - \mu_{N}(VOL_h)}{\sigma_{N}(VOL_h)}
$$

**Important**

- ❌ NO smoothing applied to volatility level  
- Level is kept raw for signal integrity  

**Purpose**

Capture:

- volatility regimes  
- structural risk levels  
- persistence of volatility states  

---

## 3.2 Volatility Dynamics (Derivatives)

### Velocity (1st derivative)

$$
VOL_{h,VEL}(t) = VOL_h(t) - VOL_h(t-1)
$$

### Acceleration (2nd derivative)

$$
VOL_{h,ACC}(t) = VOL_{h,VEL}(t) - VOL_{h,VEL}(t-1)
$$

### Smoothed derivatives

$$
VOL_{h,VEL,S}
$$

$$
VOL_{h,ACC,S}
$$

(using rolling mean)

**Important**

- ✅ Smoothing is applied **only to derivatives**  
- ❌ No smoothing on level  

**Purpose**

- detect volatility shocks  
- capture convexity / curvature  
- identify regime transitions earlier than level  

---

## 3.3 Volatility Structure

### Term structure (spreads)

$$
VOL\_TS_{s,l} = VOL_s - VOL_l
$$

Pairs:

- (21, 63)  
- (21, 126)  
- (21, 252)  
- (63, 126)  
- (63, 252)  

---

### Ratios (expansion proxy)

$$
VOL\_RATIO_{s,l} = \frac{VOL_s}{VOL_l} - 1
$$

---

### Expansion flag

$$
EXP_{s,l} = \mathbb{1}(VOL_s > VOL_l)
$$

---

**Purpose**

- detect volatility regime steepening / flattening  
- identify short-term stress vs long-term normalization  

---

## 3.4 Volatility of Volatility (VOV)

Revised definition:

$$
VOV_h = \sigma_k(VOL_h)
$$

Where:

- volatility is treated as a time series  
- rolling window captures instability of volatility itself  

---

### Z-score

$$
VOV_{h,Z}
$$

---

**Purpose**

- detect instability in volatility regimes  
- identify regime transitions  
- measure “turbulence of risk”  

---

## 3.5 Volatility Regime Indicators

### Z-score

$$
VOL_{h,Z}
$$

---

### Percentile Rank (PCTL)

$$
VOL_{h,PCTL} =
\text{PercentileRank}_{N}(VOL_h)
$$

---

### Expansion indicator

$$
EXP_{s,l} = \mathbb{1}(VOL_s > VOL_l)
$$

---

**Purpose**

- normalize volatility across time  
- identify regime extremes  
- provide bounded regime signals for modeling  

---

## 3.6 Volatility Strength Index (VSI)

Composite multi-horizon signal:

$$
VSI = \sum_{h \in H} w_h \cdot VOL_{h,Z}
$$

---

### Smoothing

$$
VSI_S = \text{MA}_k(VSI)
$$

---

**Purpose**

- aggregate multi-horizon volatility into a single signal  
- capture volatility strength across scales  
- act as a synthetic risk factor  

---

# 4. Design Principles

- All features are **continuous**  
- No hard regime labels  
- No discretization inside this layer  
- Features are **asset-independent but asset-specific**  
- Strict separation of:
  - computation  
  - normalization  
  - aggregation  

---

# 5. Known Limitations

- Rolling windows create warm-up effects  
- Long horizons reduce effective sample size  
- Extreme events can dominate statistics  
- Volatility clustering may bias normalization  
- PCTL depends heavily on window choice  

---

# 6. Downstream Usage

The Volatility Family feeds:

- Regime Detection Layer  
- Cross-Asset Systemic Risk  
- Correlation Structure  
- Portfolio Risk Models  
- Feature selection / ML models  

---

# 7. Notes on Implementation Alignment

- Derivatives (VEL, ACC) are computed explicitly  
- PCTL complements Z-score  
- VSI aggregates normalized signals  
- Smoothing is applied only to derivatives and VSI  
- Feature engine fully mirrors notebook logic  