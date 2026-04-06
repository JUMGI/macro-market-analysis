import pandas as pd

def compute_trend_signal(df, config):
    feature = config["feature"]
    return df[feature]