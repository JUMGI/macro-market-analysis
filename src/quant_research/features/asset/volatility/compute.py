# src/quant_research/features/asset/volatility/compute.py

import pandas as pd

from quant_research.features.asset.volatility.config import (
    LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS,
    VOV_WINDOWS,
    TERM_STRUCTURE_PAIRS,
    VSI_HORIZONS,
    VSI_WEIGHTS,
    VSI_SMOOTH_WINDOW,
)

# ============================================================
# 1. VOLATILITY (LEVEL)
# ============================================================

def compute_volatility(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute rolling volatility and basic normalization metrics.
    """

    feat_df = pd.DataFrame(index=data_df.index)

    for h in LOOKBACK_WINDOWS:

        col = f"VOL_{h}"

        feat_df[col] = (
            data_df["log_ret"]
            .rolling(h)
            .std()
        )

        # Z-score
        z_col = f"{col}_Z"
        feat_df[z_col] = (
            feat_df[col] - feat_df[col].rolling(NORMALIZATION_WINDOW).mean()
        ) / feat_df[col].rolling(NORMALIZATION_WINDOW).std()

        # Percentile
        pctl_col = f"{col}_PCTL"
        feat_df[pctl_col] = (
            feat_df[col]
            .rolling(NORMALIZATION_WINDOW)
            .rank(pct=True)
        )

    return feat_df


# ============================================================
# 1.5 DERIVATIVES (VEL & ACC)
# ============================================================

def compute_derivatives(vol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute velocity and acceleration of volatility.
    """

    feat_df = pd.DataFrame(index=vol_df.index)

    for h in LOOKBACK_WINDOWS:

        vol_col = f"VOL_{h}"

        if vol_col not in vol_df.columns:
            continue

        vel_col = f"{vol_col}_VEL"
        acc_col = f"{vol_col}_ACC"

        # Velocity
        feat_df[vel_col] = vol_df[vol_col].diff()

        # Acceleration
        feat_df[acc_col] = feat_df[vel_col].diff()

        # Smoothing
        smooth_window = SMOOTH_WINDOWS.get(h)

        if smooth_window:
            feat_df[f"{vel_col}_S"] = feat_df[vel_col].rolling(smooth_window).mean()
            feat_df[f"{acc_col}_S"] = feat_df[acc_col].rolling(smooth_window).mean()

    return feat_df


# ============================================================
# 2. VOLATILITY OF VOLATILITY (VOV)
# ============================================================

def compute_vov(vol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute volatility of volatility and its normalization.
    """

    feat_df = pd.DataFrame(index=vol_df.index)

    for h, window in VOV_WINDOWS.items():

        vol_col = f"VOL_{h}"
        vov_col = f"VOV_{h}"

        if vol_col not in vol_df.columns:
            continue

        feat_df[vov_col] = (
            vol_df[vol_col]
            .rolling(window)
            .std()
        )

        # Z-score
        z_col = f"{vov_col}_Z"
        feat_df[z_col] = (
            feat_df[vov_col] - feat_df[vov_col].rolling(NORMALIZATION_WINDOW).mean()
        ) / feat_df[vov_col].rolling(NORMALIZATION_WINDOW).std()

    return feat_df


# ============================================================
# 3. TERM STRUCTURE + EXPANSION
# ============================================================

def compute_term_structure(vol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute volatility term structure features.
    """

    feat_df = pd.DataFrame(index=vol_df.index)

    for short_h, long_h in TERM_STRUCTURE_PAIRS:

        short_col = f"VOL_{short_h}"
        long_col = f"VOL_{long_h}"

        if short_col not in vol_df.columns or long_col not in vol_df.columns:
            continue

        ts_col = f"VOL_TS_{short_h}_{long_h}"

        # Term structure spread
        feat_df[ts_col] = vol_df[short_col] - vol_df[long_col]

        # Z-score
        feat_df[f"{ts_col}_Z"] = (
            feat_df[ts_col] - feat_df[ts_col].rolling(NORMALIZATION_WINDOW).mean()
        ) / feat_df[ts_col].rolling(NORMALIZATION_WINDOW).std()

        # Expansion flag
        feat_df[f"EXP_{short_h}_{long_h}"] = (
            vol_df[short_col] > vol_df[long_col]
        ).astype(int)

    return feat_df


# ============================================================
# 4. VSI (Volatility Strength Index)
# ============================================================

def compute_vsi(vol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Volatility Strength Index (VSI).
    """

    feat_df = pd.DataFrame(index=vol_df.index)

    components = []
    weights = []

    for h in VSI_HORIZONS:

        col = f"VOL_{h}_Z"

        if col not in vol_df.columns:
            continue

        components.append(vol_df[col])
        weights.append(VSI_WEIGHTS.get(h, 0))

    if not components:
        return feat_df

    vsi = sum(w * c for w, c in zip(weights, components))

    feat_df["VSI"] = vsi

    if VSI_SMOOTH_WINDOW:
        feat_df["VSI_S"] = vsi.rolling(VSI_SMOOTH_WINDOW).mean()

    return feat_df


# ============================================================
# INTERNAL ORCHESTRATOR
# ============================================================

def build_volatility_features(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Internal pipeline to construct full volatility feature set.
    """

    # 1. Volatility
    vol_df = compute_volatility(data_df)

    # 1.5 Derivatives
    deriv_df = compute_derivatives(vol_df)

    # 2. VOV
    vov_df = compute_vov(vol_df)

    # 3. Term structure
    ts_df = compute_term_structure(vol_df)

    # 4. VSI
    vsi_df = compute_vsi(vol_df)

    # Final merge
    feature_df = pd.concat(
        [vol_df, deriv_df, vov_df, ts_df, vsi_df],
        axis=1
    )

    return feature_df


# ============================================================
# PUBLIC API
# ============================================================

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute volatility feature family.

    Parameters
    ----------
    df : pd.DataFrame
        Input data (must contain 'log_ret').

    Returns
    -------
    pd.DataFrame
        Volatility features:
        - index: datetime
        - columns: feature names
    """

    feature_df = build_volatility_features(df)

    # ---- enforce contract ----
    feature_df = feature_df.sort_index()
    feature_df = feature_df.loc[:, ~feature_df.columns.duplicated()]

    return feature_df

from typing import List

def get_feature_columns() -> List[str]:
    cols = []

    for h in LOOKBACK_WINDOWS:
        cols += [
            f"VOL_{h}",
            f"VOL_{h}_Z",
            f"VOL_{h}_PCTL",
            f"VOL_{h}_VEL",
            f"VOL_{h}_ACC",
        ]

        if SMOOTH_WINDOWS.get(h):
            cols.append(f"VOL_{h}_VEL_S")
            cols.append(f"VOL_{h}_ACC_S")

    # VOV
    for h in VOV_WINDOWS:
        cols.append(f"VOV_{h}")
        cols.append(f"VOV_{h}_Z")

    # Term Structure
    for short_h, long_h in TERM_STRUCTURE_PAIRS:
        cols += [
            f"VOL_TS_{short_h}_{long_h}",
            f"VOL_TS_{short_h}_{long_h}_Z",
            f"EXP_{short_h}_{long_h}",
        ]

    # VSI
    cols.append("VSI")

    if VSI_SMOOTH_WINDOW:
        cols.append("VSI_S")

    return cols