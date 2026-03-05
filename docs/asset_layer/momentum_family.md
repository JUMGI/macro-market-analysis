# Momentum Family
Layer: Asset Characterization  
Status: Research Stable  
Type: Continuous Features Only  

---

## 1. Objective

Construct a multi-horizon momentum characterization layer capturing:

- Trend level
- Trend dynamics
- Signal stability
- Cross-horizon agreement

The output is a multi-index DataFrame:

Columns:
    level 0 → feature
    level 1 → asset

Rows:
    datetime index

---

## 2. Input Assumptions

- Clean adjusted close prices
- No missing timestamps inside trading calendar
- Log returns used for momentum computation
- All calculations performed per asset independently

---

## 3. Feature Blocks

### 3.1 Momentum Level

MOM_h = log(price_t / price_{t-h})

Horizons:
- 21
- 63
- 126
- 252

Purpose:
Capture short, medium and long-term trend components.

---

### 3.2 Standardized Momentum

MOM_h_Z = rolling z-score of MOM_h

Purpose:
Time-series normalization.
Removes scale effects across assets.

---

### 3.3 Dynamics

Velocity:
MOM_h_VEL = first difference of smoothed MOM_h

Acceleration:
MOM_h_ACC = second difference of smoothed MOM_h

Smoothed variants:
MOM_h_VEL_S
MOM_h_ACC_S

Purpose:
Capture trend change and convexity.

---

### 3.4 Stability

MOM_h_STAB = rolling standard deviation of MOM_h

Purpose:
Measure trend consistency.
High stability → noisy trend.
Low stability → persistent trend.

---

### 3.5 Structural Index (MSI)

MSI_RAW = aggregate momentum structure metric
MSI_S = smoothed MSI
MSI_VEL_S = smoothed velocity
MSI_ACC_S = smoothed acceleration

Purpose:
Capture structural strength of momentum regime.

---

### 3.6 Alignment

MOM_ALIGN = mean(sign(MOM_21, 63, 126, 252))

Range:
[-1, 1]

Interpretation:
+1 → full bullish agreement
 0 → mixed
-1 → full bearish agreement

MOM_ALIGN_Z:
Filtered alignment using momentum Z-score threshold.

Purpose:
Signal confidence proxy.

---

## 4. Design Principles

- No discretization inside this layer.
- All features continuous.
- No regime labeling here.
- No allocation logic embedded.

Separation of concerns is enforced.

---

## 5. Known Limitations

- Rolling windows introduce warmup NaNs.
- Long horizons reduce effective sample size.
- Momentum inherently biased in upward drifting assets.

---

## 6. Downstream Usage

Used by:

- Volatility Family
- Cross-sectional feature engineering
- Regime Detection Layer
- Allocation Engine
