# src/quant_research/features/asset/momentum/compute.py

import pandas as pd
import numpy as np

from quant_research.features.asset.momentum.config import (
    LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS,
    MSI_WEIGHTS,
    MOM_ALIGN_THRESHOLD,
    MSI_SMOOTH_WINDOW,
)

# ============================================================
# 1. MOMENTUM LEVEL
# ============================================================

def compute_momentum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log-return based momentum over multiple horizons.
    """

    feat_df = pd.DataFrame(index=df.index)
    price = df["adj_close"]

    for h in LOOKBACK_WINDOWS:
        feat_df[f"MOM_{h}"] = np.log(price / price.shift(h))

    return feat_df


# ============================================================
# 2. MOMENTUM DERIVATIVES
# ============================================================

def compute_derivatives(mom_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute velocity and acceleration of momentum.
    """

    feat_df = pd.DataFrame(index=mom_df.index)

    for h in LOOKBACK_WINDOWS:
        col = f"MOM_{h}"

        if col not in mom_df.columns:
            continue

        vel = mom_df[col].diff()
        acc = vel.diff()

        feat_df[f"{col}_VEL"] = vel
        feat_df[f"{col}_ACC"] = acc

        window = SMOOTH_WINDOWS.get(h)

        if window:
            feat_df[f"{col}_VEL_S"] = vel.rolling(window).mean()
            feat_df[f"{col}_ACC_S"] = acc.rolling(window).mean()

    return feat_df


# ============================================================
# 3. MOMENTUM NORMALIZATION (Z + PCTL + STABILITY)
# ============================================================

def compute_normalization(mom_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize momentum using rolling statistics.
    """

    feat_df = pd.DataFrame(index=mom_df.index)

    for h in LOOKBACK_WINDOWS:
        col = f"MOM_{h}"

        if col not in mom_df.columns:
            continue

        mean = mom_df[col].rolling(NORMALIZATION_WINDOW).mean()
        std = mom_df[col].rolling(NORMALIZATION_WINDOW).std()

        z = (mom_df[col] - mean) / std

        feat_df[f"{col}_Z"] = z
        feat_df[f"{col}_PCTL"] = mom_df[col].rolling(NORMALIZATION_WINDOW).rank(pct=True)
        feat_df[f"{col}_STAB"] = mom_df[col].rolling(NORMALIZATION_WINDOW).std()

    return feat_df


# ============================================================
# 4. MSI (Momentum Strength Index)
# ============================================================

def compute_msi(mom_df: pd.DataFrame, mom_z_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Momentum Strength Index (MSI) and its derivatives.
    """

    feat_df = pd.DataFrame(index=mom_df.index)

    msi = sum(
        mom_z_df[f"MOM_{h}_Z"] * MSI_WEIGHTS.get(h, 0)
        for h in LOOKBACK_WINDOWS
        if f"MOM_{h}_Z" in mom_z_df.columns
    )

    feat_df["MSI"] = msi
    feat_df["MSI_S"] = msi.rolling(MSI_SMOOTH_WINDOW).mean()

    msi_vel = feat_df["MSI_S"].diff()
    msi_acc = msi_vel.diff()

    feat_df["MSI_VEL"] = msi_vel
    feat_df["MSI_VEL_S"] = msi_vel.rolling(MSI_SMOOTH_WINDOW).mean()
    feat_df["MSI_ACC"] = msi_acc
    feat_df["MSI_ACC_S"] = msi_acc.rolling(MSI_SMOOTH_WINDOW).mean()

    return feat_df


# ============================================================
# 5. MOMENTUM ALIGNMENT
# ============================================================

def compute_alignment(mom_df: pd.DataFrame, mom_z_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute momentum alignment metrics across horizons.
    """

    feat_df = pd.DataFrame(index=mom_df.index)

    mom_cols = [f"MOM_{h}" for h in LOOKBACK_WINDOWS if f"MOM_{h}" in mom_df.columns]
    mom_z_cols = [f"MOM_{h}_Z" for h in LOOKBACK_WINDOWS if f"MOM_{h}_Z" in mom_z_df.columns]

    # Raw alignment
    feat_df["MOM_ALIGN"] = np.sign(mom_df[mom_cols]).mean(axis=1)

    # Z-filtered alignment
    mom_z_copy = mom_z_df[mom_z_cols].copy()
    mom_z_copy[np.abs(mom_z_copy) < MOM_ALIGN_THRESHOLD] = np.nan

    signs = np.sign(mom_z_copy)
    feat_df["MOM_ALIGN_Z"] = signs.sum(axis=1) / signs.notna().sum(axis=1)

    return feat_df


# ============================================================
# INTERNAL ORCHESTRATOR
# ============================================================

def build_momentum_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Internal pipeline to construct full momentum feature set.
    """

    # 1. Momentum levels
    mom_df = compute_momentum(df)

    # 2. Derivatives
    deriv_df = compute_derivatives(mom_df)

    # 3. Normalization
    norm_df = compute_normalization(mom_df)

    # 4. MSI
    msi_df = compute_msi(mom_df, norm_df)

    # 5. Alignment
    align_df = compute_alignment(mom_df, norm_df)

    # Final merge
    feature_df = pd.concat(
        [mom_df, norm_df, deriv_df, msi_df, align_df],
        axis=1
    )

    return feature_df


# ============================================================
# PUBLIC API
# ============================================================

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute momentum feature family.

    Parameters
    ----------
    df : pd.DataFrame
        Input data (must contain 'adj_close').

    Returns
    -------
    pd.DataFrame
        Momentum features:
        - index: datetime
        - columns: feature names
    """

    feature_df = build_momentum_features(df)

    # ---- enforce contract ----
    feature_df = feature_df.sort_index()
    feature_df = feature_df.loc[:, ~feature_df.columns.duplicated()]

    return feature_df