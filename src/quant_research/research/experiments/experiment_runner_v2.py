from quant_research.data.systemic.loaders.systemic_loader import load_systemic_dataset
from quant_research.data.feature_validation.loaders.fv_loader import load_feature_validation

from quant_research.research.feature_selection.groups.grouper import FeatureGrouper
from quant_research.research.feature_selection.factory import build_feature_ranker

from quant_research.research.domains.regime.configs.loaders.regime_config_loader import load_regime_config
from quant_research.research.domains.regime.configs.mapper import map_features

from quant_research.research.domains.regime.executor import RegimeExecutor
from quant_research.research.domains.regime.evaluator import RegimeResearchEvaluator

from quant_research.research.domains.regime.search_spaces.utils import (
    extract_groups_from_regime
)

# 🔥 NEW
from quant_research.research.core.search_space.builder import SearchSpaceBuilder
from quant_research.research.core.search_space.sampler import SearchSpaceSampler

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
        # 1. LOAD DATASET
        # -------------------------
        dataset = load_systemic_dataset(config["dataset"]["id"])

        df = dataset.data
        dataset_metadata = dataset.metadata

        # -------------------------
        # 2. LOAD FV METADATA
        # -------------------------
        fv_metadata = load_feature_validation(
            config["dataset"]["id"],
            config["feature_validation"]["fv_hash"]
        )

        self._validate(dataset_metadata, fv_metadata)

        # -------------------------
        # 3. GROUP FEATURES
        # -------------------------
        grouper = FeatureGrouper()
        feature_groups = grouper.group(fv_metadata.feature_info)



        # -------------------------
        # 4. RANK FEATURES
        # -------------------------
        ranker = build_feature_ranker(
            config.get("feature_selection", {})
        )

        ranking_result = ranker.rank(
            fv_metadata.metrics,
            feature_groups
        )

        ranked_groups = ranking_result["ranked_groups"]

        print("SAMPLE FEATURE:", list(feature_groups["mom_mean_raw"])[0])

        f = list(feature_groups["mom_mean_raw"])[0]
        print("METRICS FOR FEATURE:", fv_metadata.metrics.get(f))

        print("AVAILABLE METRIC KEYS:", list(next(iter(fv_metadata.metrics.values())).keys()))
        print("WEIGHTS:", ranker.weights)

        print(ranked_groups["mom_mean_raw"])

        if not ranked_groups:
            raise ValueError("No ranked groups produced")

        # -------------------------
        # 5. LOAD REGIME TEMPLATE
        # -------------------------
        base_regime_config = load_regime_config(
            config["regime"]["config_name"]
        )

        # -------------------------
        # 6. COMPUTE HASH
        # -------------------------
        experiment_hash = compute_experiment_hash(
            config,
            dataset_metadata,
            fv_metadata
        )

        if experiment_exists(experiment_hash):
            print(f"Experiment already exists: {experiment_hash}")

        # -------------------------
        # 7. BUILD SEARCH SPACE 🔥
        # -------------------------
        required_groups = extract_groups_from_regime(base_regime_config)

        search_cfg = base_regime_config.get("search_space", {})

        builder = SearchSpaceBuilder(search_cfg)

        search_space = builder.build(
            ranked_groups=ranked_groups,
            required_groups=required_groups
        )

        # -------------------------
        # 8. SAMPLE 🔥
        # -------------------------
        sampler = SearchSpaceSampler(
            max_samples=search_cfg.get("max_samples", 10)
        )

        samples = sampler.sample(search_space)

        if not samples:
            raise ValueError("No samples generated")

        # -------------------------
        # 9. EXECUTION
        # -------------------------
        executor = RegimeExecutor()
        evaluator = RegimeResearchEvaluator(
            config=config.get("evaluation", {})
        )

        target_col = config["dataset"]["target"]

        results = []

        for i, sample in enumerate(samples):

            try:
                regime_config = map_features(
                    base_regime_config,
                    sample
                )

                regime_df = executor.run(df, regime_config)

                evaluation = evaluator.evaluate(
                    regime_df,
                    dataset,
                    target_col
                )

                results.append({
                    "sample": sample,
                    "regime_config": regime_config,
                    "metrics": evaluation["metrics"],
                    "score": evaluation["scores"]
                })

            except Exception as e:
                print(f"Sample {i} failed: {e}")

        if not results:
            raise ValueError("All samples failed")

        # -------------------------
        # 10. BEST RESULT
        # -------------------------
        best_result = max(
            results,
            key=lambda x: x["score"]["total"]
        )

        # -------------------------
        # 11. ARTIFACT
        # -------------------------
        artifact = {
            "identity": {
                "experiment_hash": experiment_hash,
                "dataset_id": config["dataset"]["id"],
                "dataset_hash": dataset_metadata["dataset_hash"],
                "fv_hash": fv_metadata.fv_hash,
                "version": "v1"
            },

            "features": {
                "feature_groups": feature_groups,
                "ranking": ranking_result,
                "search_space": search_space
            },

            "execution": {
                "n_samples": len(results),
                "results": results,
                "best_result": best_result
            },

            "config": config
        }

        # -------------------------
        # 12. STORE
        # -------------------------
        save_experiment(
            experiment_hash=experiment_hash,
            artifact=artifact
        )

        return artifact

    def _validate(self, dataset_metadata, fv_metadata):

        if dataset_metadata["dataset_hash"] != fv_metadata.dataset_hash:
            raise ValueError("Dataset hash mismatch")