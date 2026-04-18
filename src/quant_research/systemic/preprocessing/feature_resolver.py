class FeatureResolver:

    def __init__(self, catalog: dict):
        self.catalog = catalog

        self.available_features = {
            f["name"] for f in catalog["features"]
        }

    # ------------------------------------------------------------

    def resolve(self, features: list):

        required_features = set()

        # ----------------------------------------
        # SYSTEMIC FEATURES (para distinguir DAG)
        # ----------------------------------------
        systemic_names = {f.name for f in features}

        # ----------------------------------------
        # DETECT ASSET FEATURES
        # ----------------------------------------
        for feature in features:
            for inp in feature.inputs:

                # si NO es systemic → viene del panel
                if inp not in systemic_names:
                    required_features.add(inp)

        # ----------------------------------------
        # VALIDATION
        # ----------------------------------------
        missing = [
            f for f in required_features
            if f not in self.available_features
        ]

        if missing:
            raise ValueError(
                f"[FeatureResolver] Missing features in catalog: {missing}"
            )

        return sorted(required_features)