class HybridPolicy:

    def select(self, metadata, config) -> list[str]:

        weights = config.get("weights", {})
        top_k = config.get("top_k", 10)
        whitelist = config.get("whitelist", [])

        # 🔹 ranking simple
        scores = []

        for feature, values in metadata.metrics.items():

            score = 0

            for metric, w in weights.items():
                val = values.get(metric, 0)
                score += w * val

            scores.append((feature, score))

        # 🔹 ordenar
        scores.sort(key=lambda x: x[1], reverse=True)

        ranked = [f for f, _ in scores]

        # 🔹 seleccionar top_k
        selected = ranked[:top_k]

        # 🔹 agregar whitelist
        selected = list(set(selected) | set(whitelist))

        return selected