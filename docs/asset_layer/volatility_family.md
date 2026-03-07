Volatility Family
Layer: Asset Characterization
Status: Research Stable
Type: Continuous Features Only

1. Objective

Construct a multi-horizon volatility characterization layer capturing:

Volatility level
Volatility dynamics
Volatility structure across horizons
Volatility regime positioning
Volatility instability

The output is a multi-index DataFrame:

Columns:
level 0 → feature
level 1 → asset

Rows: datetime index

2. Input Assumptions

Clean adjusted close prices
No missing timestamps inside trading calendar
Log returns used for volatility computation
Annualization factor applied where required
All calculations performed per asset independently

3. Feature Blocks

3.1 Volatility Level

VOL_h = rolling standard deviation of log returns

Horizons:

21
63
126
252

Purpose: Capture short, medium and long-term risk environments.

3.2 Volatility Dynamics

Velocity:
VOL_h_CHG = first difference of volatility

Acceleration:
VOL_h_ACC = second difference of volatility

Smoothed variants:

VOL_h_CHG_S
VOL_h_ACC_S

Purpose: Capture the speed and curvature of volatility changes, identifying volatility shocks and deceleration phases.

3.3 Volatility Structure

Volatility spreads:

VOL_21_63_TERM = VOL_21 − VOL_63
VOL_21_126_TERM = VOL_21 − VOL_126
VOL_21_252_TERM = VOL_21 − VOL_252

Volatility ratios:

VOL_21_63_RATIO = VOL_21 / VOL_63 − 1
VOL_21_126_RATIO = VOL_21 / VOL_126 − 1
VOL_21_252_RATIO = VOL_21 / VOL_252 − 1

Purpose: Capture the term structure of volatility and detect short-term volatility shocks relative to longer-term baselines.

3.4 Volatility of Volatility

VOV_21_63 = rolling standard deviation of VOL_21

Purpose: Measure the instability of the volatility process itself. High values indicate turbulent or transitioning risk regimes.

3.5 Volatility Regime Indicators

Short-term regime:

VOL_21_Z = rolling z-score of VOL_21
VOL_21_PCTL = rolling percentile rank of VOL_21

Long-term regime:

VOL_252_Z = rolling z-score of VOL_252

Expansion / compression proxy:

VOL_21_63_EXP = VOL_21 / VOL_63 − 1

Purpose: Normalize volatility relative to its historical distribution and identify structural risk regimes.

4. Design Principles

No discretization inside this layer.
All features continuous.
No regime labeling here.
No allocation logic embedded.
Feature definitions remain asset-specific.

Separation of concerns is enforced.

5. Known Limitations

Rolling windows introduce warmup NaNs.
Volatility estimates depend on chosen horizons.
Extreme events can dominate rolling statistics.
Volatility clustering may produce persistent high regimes.

6. Downstream Usage

Used by:

Correlation Structure Layer
Cross-asset systemic risk analysis
Regime Detection Layer
Portfolio Risk Controls
