from abc import ABC, abstractmethod
import pandas as pd


class BaseRegimeModel(ABC):

    def __init__(self, config: dict):
        self.config = config

    def fit(self, X: pd.DataFrame):
        return self

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Returns probabilities per state.

        Output:
        index = datetime
        columns = [state_1, state_2, ...]
        values sum to 1
        """
        pass