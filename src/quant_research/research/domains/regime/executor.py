from quant_research.regimes.registry.model_registry import create_model
from quant_research.regimes.outputs.builder import RegimeOutputBuilder


class RegimeExecutor:

    def run(self, df, config):

        # 🔹 construir modelo desde registry
        model = create_model(config)

        # 🔹 probabilidades
        proba = model.predict_proba(df)

        # 🔹 construir output final
        builder = RegimeOutputBuilder()
        regime_df = builder.build(proba, config)

        return regime_df