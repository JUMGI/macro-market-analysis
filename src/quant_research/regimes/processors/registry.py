# registry.py

# registry.py

from .smoothing import RollingMeanSmoother, ExponentialSmoother
from .thresholding import ThresholdingProcessor
from .persistence import PersistenceProcessor
from .hysteresis import HysteresisProcessor
from .ensemble import EnsembleSmoother


PROCESSOR_REGISTRY = {
    "rolling_mean": RollingMeanSmoother,
    "ewm": ExponentialSmoother,
    "threshold": ThresholdingProcessor,
    "persistence": PersistenceProcessor,
    "hysteresis": HysteresisProcessor,
    "ensemble": EnsembleSmoother,
}


def create_processor(cfg):

    p_type = cfg["type"]

    if p_type not in PROCESSOR_REGISTRY:
        raise ValueError(f"Unknown processor: {p_type}")

    cls = PROCESSOR_REGISTRY[p_type]

    params = cfg.get("params", {})

    return cls(**params)


def create_pipeline(config):

    processors_cfg = config.get("processors", [])

    processors = [create_processor(p) for p in processors_cfg]

    from .pipeline import ProcessorPipeline

    return ProcessorPipeline(processors)