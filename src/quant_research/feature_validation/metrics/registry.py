from quant_research.feature_validation.metrics.stability import compute_stability
from quant_research.feature_validation.metrics.autocorr import compute_autocorr
from quant_research.feature_validation.metrics.missing import compute_missing
from quant_research.feature_validation.metrics.redundancy import compute_redundancy


METRIC_REGISTRY = {
    "stability": compute_stability,
    "autocorr": compute_autocorr,
    "missing": compute_missing,
    "redundancy": compute_redundancy,
}