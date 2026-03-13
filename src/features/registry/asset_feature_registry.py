"""
Asset Feature Registry
----------------------

Central registry for all asset-level research features.

Structure
---------
family
    group
        list[features]

Families currently implemented:

- momentum
- volatility
"""

ASSET_FEATURE_REGISTRY = {

    # ============================================================
    # MOMENTUM FAMILY
    # ============================================================

    "momentum": {

        # ----------------------------------------
        # Momentum Level
        # ----------------------------------------

        "level": [
            "MOM_21",
            "MOM_63",
            "MOM_126",
            "MOM_252",
        ],

        # ----------------------------------------
        # Standardized Momentum
        # ----------------------------------------

        "normalized": [
            "MOM_21_Z",
            "MOM_63_Z",
            "MOM_126_Z",
            "MOM_252_Z",
        ],

        # ----------------------------------------
        # Momentum Dynamics
        # ----------------------------------------

        "dynamics": [

            # velocity
            "MOM_21_VEL",
            "MOM_63_VEL",
            "MOM_126_VEL",
            "MOM_252_VEL",

            "MOM_21_VEL_S",
            "MOM_63_VEL_S",
            "MOM_126_VEL_S",
            "MOM_252_VEL_S",

            # acceleration
            "MOM_21_ACC",
            "MOM_63_ACC",
            "MOM_126_ACC",
            "MOM_252_ACC",

            "MOM_21_ACC_S",
            "MOM_63_ACC_S",
            "MOM_126_ACC_S",
            "MOM_252_ACC_S",
        ],

        # ----------------------------------------
        # Momentum Stability
        # ----------------------------------------

        "stability": [
            "MOM_21_STAB",
            "MOM_63_STAB",
            "MOM_126_STAB",
            "MOM_252_STAB",
        ],

        # ----------------------------------------
        # Momentum Alignment
        # ----------------------------------------

        "alignment": [
            "MOM_ALIGN",
            "MOM_ALIGN_Z",
        ],

        # ----------------------------------------
        # Momentum Structure Index
        # ----------------------------------------

        "structure": [
            "MSI",
            "MSI_S",
            "MSI_VEL_S",
            "MSI_ACC_S",		
        ],
                
		# ----------------------------------------
        # Momentum Regime Position
        # ----------------------------------------
 
		"regime_position": [          
            "MOM_21_PCTL",
            "MOM_63_PCTL",
            "MOM_126_PCTL",
            "MOM_252_PCTL",
		],		
		
    },


    # ============================================================
    # VOLATILITY FAMILY
    # ============================================================

    "volatility": {

        # ----------------------------------------
        # Volatility Level
        # ----------------------------------------

        "level": [
            "VOL_21",
            "VOL_63",
            "VOL_126",
            "VOL_252",
        ],

        # ----------------------------------------
        # Standardized Volatility
        # ----------------------------------------

        "normalized": [
            "VOL_21_Z",
            "VOL_63_Z",
            "VOL_126_Z",
            "VOL_252_Z",
        ],

        # ----------------------------------------
        # Volatility Dynamics
        # ----------------------------------------

        "dynamics": [

            "VOL_21_VEL",
            "VOL_21_VEL_S",
            "VOL_21_ACC",
            "VOL_21_ACC_S",

            "VOL_63_VEL",
            "VOL_63_VEL_S",
            "VOL_63_ACC",
            "VOL_63_ACC_S",

            "VOL_126_VEL",
            "VOL_126_VEL_S",
            "VOL_126_ACC",
            "VOL_126_ACC_S",

            "VOL_252_VEL",
            "VOL_252_VEL_S",
            "VOL_252_ACC",
            "VOL_252_ACC_S",
        ],

        # ----------------------------------------
        # Volatility Term Structure
        # ----------------------------------------

        "term_structure": [

            "VOL_TERM_21_63",
            "VOL_TERM_21_126",
            "VOL_TERM_21_252",

            "VOL_TERM_63_126",
            "VOL_TERM_63_252",

            "VOL_TERM_126_252",
        ],

        # ----------------------------------------
        # Volatility Ratios
        # ----------------------------------------

        "ratio_structure": [

            "VOL_RATIO_21_63",
            "VOL_RATIO_21_126",
            "VOL_RATIO_21_252",

            "VOL_RATIO_63_126",
            "VOL_RATIO_63_252",

            "VOL_RATIO_126_252",
        ],

        # ----------------------------------------
        # Volatility of Volatility
        # ----------------------------------------

        "vol_of_vol": [
            "VOV_21_63",
            "VOV_63_126",
            "VOV_21_126",
        ],

        # ----------------------------------------
        # Volatility Regime Position
        # ----------------------------------------

        "regime_position": [

            "VOL_21_PCTL",
            "VOL_63_PCTL",
            "VOL_126_PCTL",
            "VOL_252_PCTL",

            "VOL_EXP_21_63",
        ],
    },
}
