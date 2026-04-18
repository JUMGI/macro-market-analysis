class FeatureInstance:

    def __init__(self, name, type_, params, inputs):
        self.name = name
        self.type = type_
        self.params = params or {}
        self.inputs = inputs or []

        # metadata (se completa después)
        self.measure = None
        self.operator = None
        self.transform = None
        self.domain = None

    def __repr__(self):
        return f"FeatureInstance(name={self.name}, type={self.type})"