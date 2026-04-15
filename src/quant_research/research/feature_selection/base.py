class FeatureSelectionPolicy:

    def select(self, metadata, config) -> list[str]:
        raise NotImplementedError