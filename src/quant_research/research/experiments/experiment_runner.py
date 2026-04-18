from quant_research.data.systemic.loaders.systemic_loader import load_systemic_dataset
from quant_research.data.feature_validation.loaders.fv_loader import load_feature_validation

from quant_research.feature_validation.models.metadata import FeatureMetadata

from quant_research.research.feature_selection.factory import build_feature_ranker
from quant_research.research.domains.regime.configs.loaders.regime_config_loader import load_regime_config
from quant_research.research.experiments.config_builder import RegimeConfigBuilder
from quant_research.research.domains.regime.executor import RegimeExecutor

from quant_research.research.domains.regime.evaluator import RegimeResearchEvaluator
from quant_research.research.experiments.config_validator import ConfigValidator
from quant_research.research.core.experiment_hash import compute_experiment_hash

from quant_research.research.core.experiment_store import (
    save_experiment,
    experiment_exists
)



class ExperimentRunner:

    def run(self, config: dict) -> dict:
        # -------------------------
        # 0. VALIDATE CONFIG
        # -------------------------
        validator = ConfigValidator()
        validator.validate(config)

        # -------------------------
        # 1. Load dataset
        # -------------------------
        dataset = load_systemic_dataset(config["dataset"]["id"])
        df = dataset["data"]
        dataset_metadata = dataset["metadata"]

        # -------------------------
        # 2. Load Feature Validation
        # -------------------------
        fv_hash = config["feature_validation"]["fv_hash"]
        fv_metadata = load_feature_validation(config["dataset"]["id"], fv_hash)

        # -------------------------
        # 3. Validate consistency
        # -------------------------
        self._validate(dataset, fv_metadata)

        # -------------------------
        # 4. Feature Selection
        # -------------------------
        # metadata = FeatureMetadata.from_dict(fv_metadata)
        metadata = fv_metadata

        fs_config = config.get("feature_selection", {})
        ranker = build_feature_ranker(fs_config)

        ranked_groups = ranker.rank(metadata)

        if len(ranked_groups) == 0:
            raise ValueError("No ranked groups")

        print(ranked_groups)
        # -------------------------
        # 5. Load Regime Config
        # -------------------------
        regime_name = config["regime"]["config_name"]
        base_regime_config = load_regime_config(regime_name)

        config["regime_config_full"] = base_regime_config

        # 3. compute hash
        experiment_hash = compute_experiment_hash(config, dataset_metadata, fv_metadata)  

        if experiment_exists(experiment_hash):
            print(f"Experiment already exists: {experiment_hash}") 

             

        # -------------------------
        # 6. Build & validate config
        # -------------------------
        builder = RegimeConfigBuilder()

        regime_config = builder.build(
            base_regime_config,
            selected_features
        )

        # -------------------------
        # 7. Execute Regime Pipeline
        # -------------------------
        executor = RegimeExecutor()

        regime_df = executor.run(df, regime_config)

        # -------------------------
        # 8. Evaluation
        # -------------------------

        evaluator = RegimeResearchEvaluator(
            config=config.get("evaluation", {})
        )
        target_col = config["dataset"]["target"]
        evaluation = evaluator.evaluate(regime_df, dataset, target_col)

        metrics = evaluation["metrics"]
        score = evaluation["scores"]

        save_experiment(
            experiment_hash=experiment_hash,
            config=config,
            metrics=metrics,
            score=score,
            fv_metadata=fv_metadata,
            selected_features=selected_features,
            regime_df=regime_df
        )

        # -------------------------
        # 9. Return results
        # -------------------------
        return {
            "experiment_hash": experiment_hash,
            "selected_features": selected_features,
            "regime_config": regime_config,
            "regime_df": regime_df,
            "metrics": metrics,
            "score": score
        }

    # -------------------------
    # Validation
    # -------------------------

    def _validate(self, dataset: dict, fv_metadata):

        dataset_hash = dataset["metadata"]["dataset_hash"]
        fv_dataset_hash = fv_metadata.dataset_hash

        if dataset_hash != fv_dataset_hash:
            raise ValueError("Dataset hash mismatch")