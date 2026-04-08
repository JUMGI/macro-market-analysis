class ProcessorPipeline:

    def __init__(self, processors):
        self.processors = processors

    def transform(self, probs):
        for p in self.processors:
            probs = p.transform(probs)
        return probs