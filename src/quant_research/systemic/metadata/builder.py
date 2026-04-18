from quant_research.systemic.metadata.enricher import enrich_feature

class MetadataBuilder:

    def __init__(self, features):
        self.features = features

    def build(self):

        feature_map = {}
        metadata = {}

        for feature in self.features:

            enrich_feature(feature, feature_map)

            feature_map[feature.name] = feature

            metadata[feature.name] = {
                "measure": feature.measure,
                "operator": feature.operator,
                "transform": feature.transform,
                "domain": feature.domain,
                "inputs": feature.inputs,
                "params": feature.params
            }

        return metadata