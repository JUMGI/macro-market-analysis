import numpy as np
import pandas as pd


def compute_conditional_returns(regime_df, returns):
    df = regime_df.copy()
    df["ret"] = returns

    results = {}

    for regime in df["label"].unique():
        r = df[df["label"] == regime]["ret"]
        results[f"{regime}_mean_return"] = r.mean()

    return results

def compute_conditional_stats(regime_df, returns):
    df = regime_df.copy()
    df["ret"] = returns

    results = {}

    for regime in df["label"].unique():
        r = df[df["label"] == regime]["ret"]

        mean = r.mean()
        vol = r.std()

        sharpe = mean / vol if vol > 0 else 0.0

        results[f"{regime}_mean_return"] = mean
        results[f"{regime}_vol"] = vol
        results[f"{regime}_sharpe"] = sharpe

    return results

def compute_forward_returns(regime_df, returns, horizon=5):
    df = regime_df.copy()

    fwd = returns.shift(-horizon)
    df["fwd_ret"] = fwd

    results = {}

    for regime in df["label"].unique():
        r = df[df["label"] == regime]["fwd_ret"]
        results[f"{regime}_fwd_{horizon}"] = r.mean()

    return results

def compute_predictive_correlation(regime_df, returns):
    df = regime_df.copy()

    # convertir label a numérico
    mapping = {"bear": -1, "neutral": 0, "bull": 1}
    signal = df["label"].map(mapping)

    fwd = returns.shift(-1)

    corr = signal.corr(fwd)

    return {"signal_fwd_corr": corr}

def compute_drawdown_capture(regime_df, returns, threshold=-0.02):
    df = regime_df.copy()
    df["ret"] = returns

    crash_days = df["ret"] < threshold

    if crash_days.sum() == 0:
        return {"bear_capture": np.nan}

    bear_hits = (df["label"] == "bear") & crash_days

    capture = bear_hits.sum() / crash_days.sum()

    return {"bear_capture": capture}

def compute_hit_ratio(regime_df, returns, horizon=1):
    df = regime_df.copy()
    df["fwd_ret"] = returns.shift(-horizon)

    correct = 0
    total = 0

    for i in range(len(df)):
        label = df["label"].iloc[i]
        r = df["fwd_ret"].iloc[i]

        if pd.isna(r):
            continue

        if label == "bull" and r > 0:
            correct += 1
            total += 1
        elif label == "bear" and r < 0:
            correct += 1
            total += 1
        elif label in ["bull", "bear"]:
            total += 1

    return {"hit_ratio": correct / total if total > 0 else 0.0}

def compute_transition_pnl(regime_df, returns, horizon=5):
    df = regime_df.copy()
    df["fwd_ret"] = returns.shift(-horizon)

    transitions = df["label"] != df["label"].shift(1)

    pnl = []

    for i in range(len(df)):
        if not transitions.iloc[i]:
            continue

        label = df["label"].iloc[i]
        r = df["fwd_ret"].iloc[i]

        if pd.isna(r):
            continue

        # estrategia simple
        if label == "bull":
            pnl.append(r)
        elif label == "bear":
            pnl.append(-r)

    if len(pnl) == 0:
        return {"transition_pnl": 0.0}

    return {"transition_pnl": sum(pnl) / len(pnl)}

def compute_regime_drawdown(regime_df, returns):
    df = regime_df.copy()
    df["ret"] = returns

    results = {}

    for regime in df["label"].unique():
        r = df[df["label"] == regime]["ret"]

        if len(r) == 0:
            continue

        cum = (1 + r).cumprod()
        peak = cum.cummax()
        dd = (cum - peak) / peak

        results[f"{regime}_max_dd"] = dd.min()

    return results