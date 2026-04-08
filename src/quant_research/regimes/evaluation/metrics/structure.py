import pandas as pd


def compute_persistence(regime_df: pd.DataFrame) -> float:
    labels = regime_df["label"]

    durations = []
    current = labels.iloc[0]
    count = 1

    for i in range(1, len(labels)):
        if labels.iloc[i] == current:
            count += 1
        else:
            durations.append(count)
            current = labels.iloc[i]
            count = 1

    durations.append(count)

    return sum(durations) / len(durations)


def compute_transition_rate(regime_df: pd.DataFrame) -> float:
    labels = regime_df["label"]
    transitions = (labels != labels.shift(1)).sum()
    return transitions / len(labels)


def compute_entropy_mean(regime_df: pd.DataFrame) -> float:
    return regime_df["entropy"].mean()