from quant_research.regimes.models.rule_based.model import RuleBasedModel
from quant_research.regimes.models.rule_based.condition_evaluator import ConditionEvaluator
from quant_research.regimes.models.rule_based.rule_evaluator import RuleEvaluator
from quant_research.regimes.models.rule_based.scorer import RegimeScorer


def _create_rule_based(config):

    return RuleBasedModel(
        config=config,
        condition_evaluator=ConditionEvaluator(),
        rule_evaluator=RuleEvaluator(),
        scorer=RegimeScorer()
    )


MODEL_REGISTRY = {
    "rule_based": _create_rule_based,
}


def create_model(config: dict):

    model_type = config["model"]["type"]

    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model type: {model_type}")

    return MODEL_REGISTRY[model_type](config)