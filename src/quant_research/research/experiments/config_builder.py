class RegimeConfigBuilder:

    def build(self, base_config: dict, selected_features: list[str]) -> dict:

        config = base_config.copy()

        self._validate_features(config, selected_features)

        return config

    def _validate_features(self, config: dict, selected_features: list[str]):

        model = config.get("model", {})
        regimes = model.get("regimes", [])

        missing = []

        for regime in regimes:
            for rule in regime.get("rules", []):
                for cond in rule.get("conditions", []):

                    feature = cond.get("feature")

                    if feature not in selected_features:
                        missing.append(feature)

        if missing:
            raise ValueError(
                f"Model uses features not selected: {set(missing)}"
            )