# regimes/validation/feature_validator.py

class FeatureValidator:

    def validate(self, config: dict, systemic_metadata: dict) -> None:
        """
        Validate that all features required by the regime config
        exist in the systemic dataset.

        Raises:
            ValueError: if any feature is missing
        """

        required_features = self._extract_features(config)
        available_features = self._get_available_features(systemic_metadata)

        missing = sorted(required_features - available_features)

        if missing:
            raise ValueError(
                self._build_error_message(missing, available_features)
            )

    # -------------------------
    # INTERNALS
    # -------------------------
    def _extract_features(self, config: dict) -> set:

        features = set()

        model_cfg = config.get("model", {})
        regimes = model_cfg.get("regimes", [])

        # soporta list o dict (robusto)
        if isinstance(regimes, dict):
            regimes_iter = regimes.values()
        else:
            regimes_iter = regimes

        for regime in regimes_iter:

            rules = regime.get("rules", [])

            for rule in rules:
                conditions = rule.get("conditions", [])

                for cond in conditions:
                    feature = cond.get("feature")

                    if feature:
                        features.add(feature)
                    if not features:
                        raise ValueError(
                            "[FeatureValidator] No features extracted. Check config structure."
                        )

        return features

  

    def _get_available_features(self, systemic_metadata: dict) -> set:
        """
        Extract available features from systemic metadata.
        """

        return set(
            systemic_metadata
            .get("systemic", {})
            .get("features", [])
        )

    def _build_error_message(self, missing, available) -> str:
        return (
            "\n[FeatureValidator] Missing features in systemic dataset:\n"
            f"{missing}\n\n"
            "Available features:\n"
            f"{sorted(available)}\n"
        )