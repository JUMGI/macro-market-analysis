def compute_score(metrics: dict, weights: dict) -> float:
    score = 0.0

    for k, w in weights.items():
        score += w * metrics.get(k, 0.0)

    return score

def compute_grouped_score(metrics, config):

    structure = config["structure"]
    economic = config["economic"]
    decision = config["decision"]

    def score_group(group_config):
        s = 0.0
        for k, w in group_config.items():
            s += w * metrics.get(k, 0.0)
        return s

    structure_score = score_group(structure)
    economic_score = score_group(economic)
    decision_score = score_group(decision)

    total = (
        config["weights"]["structure"] * structure_score +
        config["weights"]["economic"] * economic_score +
        config["weights"]["decision"] * decision_score
    )

    return {
        "total": total,
        "structure": structure_score,
        "economic": economic_score,
        "decision": decision_score
    }