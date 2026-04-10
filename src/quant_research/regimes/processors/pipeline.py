# pipeline.py

class ProcessorPipeline:

    def __init__(self, processors):
        self.processors = processors or []

    def apply(self, probs):

        for p in self.processors:
            probs = p.apply(probs)

        return probs