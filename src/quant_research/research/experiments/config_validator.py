class ConfigValidator:

    def validate(self, config: dict):

        self._validate_root(config)
        self._validate_dataset(config["dataset"])
        self._validate_feature_validation(config)
        self._validate_regime(config["regime"])
        self._validate_evaluation(config["evaluation"])

    # -------------------------
    # ROOT
    # -------------------------

    def _validate_root(self, config):

        required = ["dataset", "regime", "evaluation"]

        for key in required:
            if key not in config:
                raise ValueError(f"Missing required config section: {key}")

    # -------------------------
    # DATASET
    # -------------------------

    def _validate_dataset(self, dataset):

        if "id" not in dataset:
            raise ValueError("dataset.id is required")

        if "target" not in dataset:
            raise ValueError("dataset.target is required")

    # -------------------------
    # FEATURE VALIDATION
    # -------------------------

    def _validate_feature_validation(self, config):

        if "feature_validation" not in config:
            return  # opcional en V1

        fv = config["feature_validation"]

        if "fv_hash" not in fv:
            raise ValueError("feature_validation.fv_hash is required")

    # -------------------------
    # REGIME
    # -------------------------

    def _validate_regime(self, regime):

        if "config_name" not in regime:
            raise ValueError("regime.config_name is required")

    # -------------------------
    # EVALUATION
    # -------------------------

    def _validate_evaluation(self, evaluation):

        required_groups = ["structure", "economic", "decision", "weights"]

        for g in required_groups:
            if g not in evaluation:
                raise ValueError(f"evaluation.{g} is required")

        # validar pesos de grupos
        weights = evaluation["weights"]

        for g in ["structure", "economic", "decision"]:
            if g not in weights:
                raise ValueError(f"evaluation.weights.{g} is required")

    def _validate_feature_selection(self, config):

        if "feature_selection" not in config:
            return

        fs = config["feature_selection"]

        if "method" not in fs:
            raise ValueError("feature_selection.method is required")

        if fs["method"] == "hybrid":

            if "weights" not in fs:
                raise ValueError("feature_selection.weights is required")

            if "top_k" not in fs:
                raise ValueError("feature_selection.top_k is required")