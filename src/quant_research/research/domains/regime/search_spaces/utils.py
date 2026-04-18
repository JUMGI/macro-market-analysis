def extract_groups_from_regime(regime_config: dict) -> set[str]:

    groups = set()

    regimes = regime_config.get("model", {}).get("regimes", [])

    for regime in regimes:
        for rule in regime.get("rules", []):
            for cond in rule.get("conditions", []):
                feature = cond.get("feature")

                if feature:
                    groups.add(feature)

    return groups