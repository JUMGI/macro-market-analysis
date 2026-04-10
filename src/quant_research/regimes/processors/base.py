# base.py

import pandas as pd

class BaseProcessor:

    def apply(self, probs: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError