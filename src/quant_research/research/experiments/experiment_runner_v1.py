from quant_research.data.systemic.loaders.systemic_loader import load_systemic_dataset
from quant_research.data.feature_validation.loaders.fv_loader import load_feature_validation

from quant_research.research.feature_selection.groups.grouper import FeatureGrouper
from quant_research.research.feature_selection.factory import build_feature_ranker

from quant_research.research.domains.regime.configs.loaders.regime_config_loader import load_regime_config
from quant_research.research.domains.regime.sampling.sampler import RegimeFeatureSampler
from quant_research.research.domains.regime.configs.mapper import map_features

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
        # 1. Load dataset (NEW CONTRACT)
        # -------------------------
        dataset = load_systemic_dataset(config["dataset"]["id"])

        df = dataset.data
        df_z = dataset.data_z  # 🔥 disponible si lo necesitás después
        dataset_metadata = dataset.metadata

        # -------------------------
        # 2. Load Feature Validation
        # -------------------------
        fv_hash = config["feature_validation"]["fv_hash"]
        fv_metadata = load_feature_validation(config["dataset"]["id"], fv_hash)

        # -------------------------
        # 3. Validate consistency
        # -------------------------
        self._validate(dataset_metadata, fv_metadata)

        # -------------------------
        # 4. Feature Ranking
        # -------------------------
        fs_config = config.get("feature_selection", {})
        ranker = build_feature_ranker(fs_config)

        feature_info = fv_metadata.feature_info

        grouper = FeatureGrouper()
        groups = grouper.group(feature_info)

        ranked_groups = ranker.rank(fv_metadata.metrics, groups)

        if not ranked_groups:
            raise ValueError("No ranked groups produced")

        # -------------------------
        # 5. Load Regime Template
        # -------------------------
        regime_name = config["regime"]["config_name"]
        base_regime_config = load_regime_config(regime_name)

        config["regime_config_full"] = base_regime_config

        # -------------------------
        # 6. Compute Experiment Hash
        # -------------------------
        experiment_hash = compute_experiment_hash(
            config,
            dataset_metadata,
            fv_metadata
        )

        if experiment_exists(experiment_hash):
            print(f"Experiment already exists: {experiment_hash}")

        # -------------------------
        # 7. Sampling (Search Space)
        # -------------------------
        sampler = RegimeFeatureSampler(
            top_k=config.get("search_space", {}).get("top_k", 3),
            max_samples=config.get("search_space", {}).get("max_samples", 10)
        )

        samples = sampler.sample(base_regime_config, ranked_groups)

        if not samples:
            raise ValueError("No samples generated")

        # -------------------------
        # 8. Execution Loop
        # -------------------------
        executor = RegimeExecutor()
        evaluator = RegimeResearchEvaluator(
            config=config.get("evaluation", {})
        )

        target_col = config["dataset"]["target"]

        results = []

        for i, sample in enumerate(samples):

            try:
                regime_config = map_features(base_regime_config, sample)

                regime_df = executor.run(df, regime_config)

                evaluation = evaluator.evaluate(regime_df, dataset, target_col)

                result = {
                    "sample": sample,
                    "regime_config": regime_config,
                    "metrics": evaluation["metrics"],
                    "score": evaluation["scores"]
                }

                results.append(result)

            except Exception as e:
                print(f"Sample {i} failed: {e}")

        if not results:
            raise ValueError("All samples failed")

        # -------------------------
        # 9. Select Best Result
        # -------------------------
        best_result = max(
            results,
            key=lambda x: x["score"]["total"]
        )

        # -------------------------
        # 10. Persist Experiment
        # -------------------------
        save_experiment(
            experiment_hash=experiment_hash,
            config=config,
            results=results,
            best_result=best_result,
            fv_metadata=fv_metadata
        )

        # -------------------------
        # 11. Return
        # -------------------------
        return {
            "experiment_hash": experiment_hash,
            "n_samples": len(results),
            "best": best_result,
            "results": results
        }

    # -------------------------
    # Validation
    # -------------------------
    def _validate(self, dataset_metadata, fv_metadata):

        dataset_hash = dataset_metadata["dataset_hash"]
        fv_dataset_hash = fv_metadata.dataset_hash

        if dataset_hash != fv_dataset_hash:
            raise ValueError("Dataset hash mismatch")