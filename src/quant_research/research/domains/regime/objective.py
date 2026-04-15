def compute_score(metrics: dict, weights: dict) -> float:
    score = 0.0

    for k, w in weights.items():
        score += w * metrics.get(k, 0.0)

    return score

def compute_grouped_score(metrics: dict, config: dict) -> dict:

    structure_cfg = config.get("structure", {})
    economic_cfg = config.get("economic", {})
    decision_cfg = config.get("decision", {})
    group_weights = config.get("weights", {})

    def score_group(group_config):
        s = 0.0
        for k, w in group_config.items():
            s += w * metrics.get(k, 0.0)
        return s

    structure_score = score_group(structure_cfg)
    economic_score = score_group(economic_cfg)
    decision_score = score_group(decision_cfg)

    total = (
        group_weights.get("structure", 0.0) * structure_score +
        group_weights.get("economic", 0.0) * economic_score +
        group_weights.get("decision", 0.0) * decision_score
    )

    return {
        "total": total,
        "structure": structure_score,
        "economic": economic_score,
        "decision": decision_score
    }