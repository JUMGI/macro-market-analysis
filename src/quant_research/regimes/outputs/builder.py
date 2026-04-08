import pandas as pd
from quant_research.regimes.outputs.metrics import (
    compute_confidence,
    compute_entropy,
)


class RegimeOutputBuilder:

    def build(self, probs: pd.DataFrame, config: dict) -> pd.DataFrame:
        df = probs.copy()

        label = df.idxmax(axis=1)
        confidence = compute_confidence(df)
        entropy = compute_entropy(df)

        df["label"] = label
        df["confidence"] = confidence
        df["entropy"] = entropy

        return df