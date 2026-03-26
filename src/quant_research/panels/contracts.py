# ============================================================
# PANEL CONTRACTS
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# COLUMN LEVEL NAMES
# ------------------------------------------------------------

FEATURE_LEVEL = "feature"
ASSET_LEVEL = "asset"

COLUMN_NAMES = [FEATURE_LEVEL, ASSET_LEVEL]


# ------------------------------------------------------------
# ENFORCE PANEL STRUCTURE
# ------------------------------------------------------------

def enforce_panel_contract(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce the canonical panel structure.

    Expected structure:
        - index: datetime
        - columns: MultiIndex (feature, asset)
        - column names: ["feature", "asset"]

    This function:
        - ensures MultiIndex columns
        - reorders levels if needed
        - sets level names
        - sorts columns

    Parameters
    ----------
    panel : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    if not isinstance(panel.columns, pd.MultiIndex):
        raise ValueError("Panel columns must be a MultiIndex")

    # --------------------------------------------------------
    # DETECT CURRENT STRUCTURE
    # --------------------------------------------------------

    level0_sample = panel.columns.get_level_values(0)[0]
    level1_sample = panel.columns.get_level_values(1)[0]

    # heuristic: features are usually strings like "MOM_63"
    is_feature_first = isinstance(level0_sample, str) and "_" in level0_sample

    # --------------------------------------------------------
    # REORDER IF NEEDED
    # --------------------------------------------------------

    if not is_feature_first:
        panel = panel.swaplevel(0, 1, axis=1)

    # --------------------------------------------------------
    # SET NAMES
    # --------------------------------------------------------

    panel.columns.names = COLUMN_NAMES

    # --------------------------------------------------------
    # SORT COLUMNS
    # --------------------------------------------------------

    panel = panel.sort_index(axis=1)

    return panel


# ------------------------------------------------------------
# VALIDATE PANEL STRUCTURE
# ------------------------------------------------------------

def validate_panel_contract(panel: pd.DataFrame) -> None:
    """
    Validate that a panel follows the canonical structure.

    Raises
    ------
    ValueError if validation fails.
    """

    if not isinstance(panel.columns, pd.MultiIndex):
        raise ValueError("Panel columns must be MultiIndex")

    if list(panel.columns.names) != COLUMN_NAMES:
        raise ValueError(
            f"Invalid column names: {panel.columns.names}, "
            f"expected {COLUMN_NAMES}"
        )