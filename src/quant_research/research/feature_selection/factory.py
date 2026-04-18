from quant_research.research.feature_selection.ranking.hybrid_ranker_v1 import HybridRanker


def build_feature_ranker(config: dict):

    ranker_name = config.get("ranker", "hybrid")

    if ranker_name == "hybrid":
        return HybridRanker(config)  # 🔥 PASAR TODO

    raise ValueError(f"Unknown ranker: {ranker_name}")