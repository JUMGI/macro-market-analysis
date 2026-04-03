from .mean import mean
from .trend import trend
from .dispersion import dispersion
from .correlation import correlation
from .breadth import breadth
from .skew import skew
from .volatility import volatility
from .zscore import zscore
from .percentile import percentile
from .range import range_
from .volatility import volatility
from .ts_volatility import ts_volatility

AGGREGATOR_REGISTRY = {
    "mean": mean,
    "trend": trend,
    "dispersion": dispersion,
    "correlation": correlation,
    "breadth": breadth,
    "skew": skew,
    "volatility": volatility,
    "zscore": zscore,
    "percentile": percentile,
    "range": range_,
    "volatility": volatility,
    "ts_volatility": ts_volatility,
}