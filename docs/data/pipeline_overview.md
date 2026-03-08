# Quant Research Platform — Data Pipeline Overview

This document summarizes the **data flow** from raw market data to processed datasets ready for feature engineering.

---

## 1️⃣ Raw Market Data (`data/raw/`)

- Assets: ETFs, Equities, Crypto  
- Daily Adjusted Close Prices  
- Panel Format: Date x Ticker  
- Notes:
  - Different start dates for each asset
  - Missing data allowed
  - 5-day trading for equities, 7-day for crypto

---

## 2️⃣ Data Loading (`01_data_pipeline.ipynb`)

- Load all tickers via `yfinance`  
- Rename columns via mapping (`raw ticker → asset code`)  
- No cleaning yet; preserves raw data as downloaded  

---

## 3️⃣ Core Computation

- **Price Cleaning & Calendar Alignment**
  - Sort prices chronologically  
  - Forward-fill **only equities** (SPY, QQQ, XLE) with `limit=5`  
  - Drop initial NaNs after reindexing  
  - **Crypto assets (BTC)** maintain real weekend values  

- **Return Computation**
  - Log returns: `r_t = log(P_t / P_{t-1})`  
  - No forward-filling of returns  
  - Rolling windows naturally introduce warm-up NaNs  

- **Diagnostics / Validation**
  - Monotonic index check  
  - No remaining NaNs after initial cleaning  
  - Extreme returns kept for volatility analysis  
  - Asset columns and shapes validated  

---

## 4️⃣ Storage

- **Processed datasets** stored in Parquet:  
  - `prices.parquet` → cleaned price series  
  - `returns.parquet` → log returns  
- Wide panel format (Date x Asset)  
- Versioning recommended for reproducibility  

---

## 5️⃣ Feature Engineering (`02_asset_characterization.ipynb`)

- Compute features such as:
  - Momentum
  - Volatility
  - Normalized / scaled features  
- Rolling windows applied with warm-up NaNs handled  
- Cross-asset and systemic features computed  

---

## 6️⃣ Systemic Features (`03_systemic_features.ipynb`)

- Breadth, Dispersion, Correlation, Market Regimes  
- Exported to feature registry or long panel format for ML  
- Compatible with wide → long transformation  

---

## 7️⃣ Pipeline Notes

- Forward-fill **limited** avoids inflating equity volatility  
- **Crypto weekend data preserved** for liquidity and proxy signals  
- All datasets aligned on a **full calendar union**  
- Parquet storage ensures **fast loading, reproducibility, and versioning**  
- Designed for gradual evolution:
  1. Research notebooks
  2. Modular `src/` functions
  3. Production research system
