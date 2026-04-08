def compute_prob_spread(regime_df):
    prob_cols = [c for c in regime_df.columns if c not in ["label", "entropy", "confidence"]]

    probs = regime_df[prob_cols]

    top1 = probs.max(axis=1)
    top2 = probs.apply(lambda x: x.nlargest(2).iloc[-1], axis=1)

    return (top1 - top2).mean()