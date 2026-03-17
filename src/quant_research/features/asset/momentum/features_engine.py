from quant_research.features.asset.momentum.config import (
    LOOKBACK_WINDOWS,
    NORMALIZATION_WINDOW,
    SMOOTH_WINDOWS,
    MSI_WEIGHTS,
    MOM_ALIGN_THRESHOLD,
    MSI_SMOOTH_WINDOW,
)

# ============================================================
# Momentum Feature Engine
# ============================================================

import pandas as pd
import numpy as np


def compute_momentum_features(
    df_raw: pd.DataFrame,
    lookback_windows: list,
    normalization_window: int,
    smooth_windows: dict,
    msi_weights: dict,
    mom_align_threshold: float,
    msi_smooth_window: int = 5,
) -> pd.DataFrame:

    price = df_raw["adj_close"]

    # ============================================================
    # DAG STORAGE
    # ============================================================
    mom = {}
    mom_pctl = {}
    vel = {}
    acc = {}
    mom_z = {}
    vel_s = {}
    acc_s = {}

    # ============================================================
    # 1. MOMENTUM
    # ============================================================
    for h in lookback_windows:
        mom[h] = np.log(price / price.shift(h))

    # ============================================================
    # 2. PERCENTILE (VECTORIZED)
    # ============================================================
    for h in lookback_windows:
        mom_pctl[h] = mom[h].rolling(normalization_window).rank(pct=True)

    # ============================================================
    # 3. DERIVATIVES
    # ============================================================
    for h in lookback_windows:
        vel[h] = mom[h].diff()
        acc[h] = vel[h].diff()

    # ============================================================
    # 4. Z-SCORE
    # ============================================================
    for h in lookback_windows:
        mean = mom[h].rolling(normalization_window).mean()
        std = mom[h].rolling(normalization_window).std()
        mom_z[h] = (mom[h] - mean) / std

    # ============================================================
    # 5. SMOOTHING
    # ============================================================
    for h in lookback_windows:
        window = smooth_windows.get(h)

        if window is not None:
            vel_s[h] = vel[h].rolling(window).mean()
            acc_s[h] = acc[h].rolling(window).mean()

    # ============================================================
    # BUILD FEATURE DF
    # ============================================================
    df_feat = pd.DataFrame(index=df_raw.index)

    # -------------------------
    # Momentum + derivatives
    # -------------------------
    for h in lookback_windows:
        df_feat[f"MOM_{h}"] = mom[h]

        # PCTL
        df_feat[f"MOM_{h}_PCTL"] = mom_pctl[h]

        # Derivatives
        df_feat[f"MOM_{h}_VEL"] = vel[h]
        df_feat[f"MOM_{h}_ACC"] = acc[h]

        if h in vel_s:
            df_feat[f"MOM_{h}_VEL_S"] = vel_s[h]
        if h in acc_s:
            df_feat[f"MOM_{h}_ACC_S"] = acc_s[h]

        # Z-score
        df_feat[f"MOM_{h}_Z"] = mom_z[h]

        # Stability
        df_feat[f"MOM_{h}_STAB"] = mom[h].rolling(normalization_window).std()

    # ============================================================
    # 6. MSI
    # ============================================================
    msi = sum(
        mom_z[h] * w
        for h, w in msi_weights.items()
        if h in mom_z
    )

    df_feat["MSI"] = msi

    # -------------------------
    # MSI Smoothed
    # -------------------------
    msi_s = msi.rolling(msi_smooth_window).mean()
    df_feat["MSI_S"] = msi_s

    # -------------------------
    # MSI Derivatives
    # -------------------------
    msi_vel = msi_s.diff()
    df_feat["MSI_VEL"] = msi_vel

    df_feat["MSI_VEL_S"] = msi_vel.rolling(msi_smooth_window).mean()

    msi_acc = msi_vel.diff()
    df_feat["MSI_ACC"] = msi_acc

    df_feat["MSI_ACC_S"] = msi_acc.rolling(msi_smooth_window).mean()

    # ============================================================
    # 7. MOM_ALIGN
    # ============================================================
    mom_df = pd.concat(mom, axis=1)
    mom_df.columns = [f"MOM_{h}" for h in lookback_windows]

    df_feat["MOM_ALIGN"] = np.sign(mom_df).mean(axis=1)

    # ============================================================
    # 8. MOM_ALIGN_Z
    # ============================================================
    mom_z_df = pd.concat(mom_z, axis=1)
    mom_z_df.columns = [f"MOM_{h}_Z" for h in lookback_windows]

    # threshold → NaN (no contaminar el promedio)
    mom_z_df = mom_z_df.copy()
    mom_z_df[np.abs(mom_z_df) < mom_align_threshold] = np.nan

    signs = np.sign(mom_z_df)
    align_z = signs.sum(axis=1) / signs.notna().sum(axis=1)

    df_feat["MOM_ALIGN_Z"] = align_z

    return df_feat