class FeatureResolver:

    def __init__(self, catalog: dict):
        self.catalog = catalog

        self.available_features = {
            f["name"] for f in catalog["features"]
        }

    # ------------------------------------------------------------

    def resolve(self, configs: list):

        required_features = set()

        for cfg in configs:

            # ----------------------------------------
            # SOLO features del panel
            # ----------------------------------------
            if "features" in cfg:
                required_features.update(cfg["features"])

            # ----------------------------------------
            # IMPORTANTE:
            # NO validar "input"
            # porque es dependencia interna systemic
            # ----------------------------------------

        # ----------------------------------------
        # VALIDATION (solo asset features)
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