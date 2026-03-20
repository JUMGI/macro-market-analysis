# ============================================================
# universe_registry.py
# ============================================================

from dataclasses import dataclass
from typing import List, Optional, Dict

# ============================================================
# Asset dataclass
# ============================================================

@dataclass
class Asset:
    symbol: str         # ticker o nombre corto
    asset_type: str     # 'equity', 'etf', 'crypto', 'commodity', 'bond'
    market: str         # 'US', 'Global', etc.
    sector: Optional[str] = None
    group: Optional[str] = None
    currency: Optional[str] = "USD"  # default USD
    yfinance_ticker: Optional[str] = None  # si difiere del symbol

    def get_ticker(self) -> str:
        """Return yfinance ticker if defined, else symbol"""
        return self.yfinance_ticker or self.symbol

# ============================================================
# Define universe
# ============================================================

ASSET_UNIVERSE: List[Asset] = [
    Asset("SPY", "etf", "US", sector="Large Cap", group="equity"),
    Asset("QQQ", "etf", "US", sector="Tech", group="equity"),
    Asset("XLE", "etf", "US", sector="Energy", group="equity"),
    Asset("XLF", "etf", "US", sector="Financials", group="equity"),
    Asset("IWM", "etf", "US", sector="Small Cap", group="equity"),
    Asset("VTI", "etf", "US", sector="Total Market", group="equity"),
    Asset("TLT", "bond", "US", sector="Long-term Treasury", group="bond"),
    Asset("GLD", "commodity", "US", sector="Gold", group="commodity"),
    Asset("BTC", "crypto", "Global", group="crypto", yfinance_ticker="BTC-USD"),
    Asset("ETH", "crypto", "Global", group="crypto", yfinance_ticker="ETH-USD"),
]

# ============================================================
# Helper functions
# ============================================================

def get_tickers(asset_list: Optional[List[Asset]] = None) -> List[str]:
    """Return list of yfinance tickers for given assets, default all"""
    assets = asset_list if asset_list is not None else ASSET_UNIVERSE
    return [a.get_ticker() for a in assets]

def get_assets_by_type(asset_type: str, asset_list: Optional[List[Asset]] = None) -> List[Asset]:
    """Return list of Asset objects matching a given type"""
    assets = asset_list if asset_list is not None else ASSET_UNIVERSE
    return [a for a in assets if a.asset_type == asset_type]

def get_groups_by_type(asset_list: Optional[List[Asset]] = None) -> Dict[str, List[Asset]]:
    """Return dictionary grouping assets by type"""
    assets = asset_list if asset_list is not None else ASSET_UNIVERSE
    groups: Dict[str, List[Asset]] = {}
    for a in assets:
        groups.setdefault(a.asset_type, []).append(a)
    return groups
def get_symbols(asset_list=None):
    assets = asset_list if asset_list else ASSET_UNIVERSE
    return [a.symbol for a in assets]