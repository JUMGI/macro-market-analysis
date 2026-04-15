from quant_research.regimes.evaluation.evaluator import RegimeEvaluator


class RegimeResearchEvaluator:

    def __init__(self, config: dict):
        self.config = config
        
    def evaluate(self, regime_df, dataset, target_col) -> dict:

        # 🔹 usar evaluator REAL
        evaluator = RegimeEvaluator(self.config)

                
        returns = dataset["data"][target_col]
        results = evaluator.evaluate(regime_df, returns)

        

        return results