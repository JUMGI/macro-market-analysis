# src/quant_research/data/registry/universe_registry.py

from dataclasses import dataclass
from typing import List, Optional, Dict


# ============================================================
# Asset Definition
# ============================================================

@dataclass(frozen=True)
class Asset:
    """
    Immutable asset definition used across the platform.
    """

    symbol: str
    asset_type: str        # 'etf', 'equity', 'crypto', etc.
    market: str            # 'US', 'Global', etc.

    sector: Optional[str] = None
    asset_class: Optional[str] = None   # renamed from 'group'
    currency: str = "USD"

    yfinance_ticker: Optional[str] = None

    def get_ticker(self) -> str:
        """Return yfinance ticker if defined, else symbol."""
        return self.yfinance_ticker or self.symbol


# ============================================================
# Universe Definition
# ============================================================

_ASSETS: List[Asset] = [
    Asset("SPY", "etf", "US", sector="Large Cap", asset_class="equity"),
    Asset("QQQ", "etf", "US", sector="Tech", asset_class="equity"),
    Asset("XLE", "etf", "US", sector="Energy", asset_class="equity"),
    Asset("XLF", "etf", "US", sector="Financials", asset_class="equity"),
    Asset("IWM", "etf", "US", sector="Small Cap", asset_class="equity"),
    Asset("VTI", "etf", "US", sector="Total Market", asset_class="equity"),
    Asset("TLT", "bond", "US", sector="Treasury", asset_class="bond"),
    Asset("GLD", "commodity", "US", sector="Gold", asset_class="commodity"),
    Asset("BTC", "crypto", "Global", asset_class="crypto", yfinance_ticker="BTC-USD"),
    Asset("ETH", "crypto", "Global", asset_class="crypto", yfinance_ticker="ETH-USD"),
]


# ============================================================
# Indexing (critical for scalability)
# ============================================================

_ASSET_MAP: Dict[str, Asset] = {a.symbol: a for a in _ASSETS}


# ============================================================
# Public API
# ============================================================

def get_all_assets() -> List[Asset]:
    return list(_ASSETS)


def get_asset(symbol: str) -> Asset:
    if symbol not in _ASSET_MAP:
        raise ValueError(f"Asset not found: {symbol}")
    return _ASSET_MAP[symbol]


def get_symbols() -> List[str]:
    return list(_ASSET_MAP.keys())


def get_tickers() -> List[str]:
    return [a.get_ticker() for a in _ASSETS]


def get_by_asset_type(asset_type: str) -> List[Asset]:
    return [a for a in _ASSETS if a.asset_type == asset_type]


def get_by_asset_class(asset_class: str) -> List[Asset]:
    return [a for a in _ASSETS if a.asset_class == asset_class]


def group_by_asset_type() -> Dict[str, List[Asset]]:
    groups: Dict[str, List[Asset]] = {}
    for a in _ASSETS:
        groups.setdefault(a.asset_type, []).append(a)
    return groups