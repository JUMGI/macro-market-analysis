# src/quant_research/features/validation/core_validator.py

import pandas as pd


def validate_features(
    df_expected: pd.DataFrame,
    df_stored: pd.DataFrame,
    tolerance: float,
    verbose: bool = True,
) -> dict:
    """
    Generic feature validation engine.

    Compares expected vs stored feature DataFrames.

    Parameters
    ----------
    df_expected : pd.DataFrame
        Recomputed features (source of truth)
    df_stored : pd.DataFrame
        Stored features (e.g. parquet)
    tolerance : float
        Numerical tolerance for differences
    verbose : bool
        Print diagnostics

    Returns
    -------
    dict
        {
            "status": "PASS" | "WARNING",
            "n_issues": int,
            "failed_features": list[str]
        }
    """

    # --------------------------------------------------------
    # Align columns
    # --------------------------------------------------------
    expected_cols = set(df_expected.columns)
    stored_cols = set(df_stored.columns)

    common_cols = sorted(expected_cols & stored_cols)
    extra_cols = sorted(stored_cols - expected_cols)
    missing_cols = sorted(expected_cols - stored_cols)

    all_ok = True
    failed_features = []

    # --------------------------------------------------------
    # Compare values
    # --------------------------------------------------------
    for col in common_cols:

        diff = (df_expected[col] - df_stored[col]).abs().max()

        if pd.isna(diff):
            if verbose:
                print(f"{col}: SKIP (all NaN)")
            continue

        if diff < tolerance:
            if verbose:
                print(f"{col}: OK")
        else:
            if verbose:
                print(f"{col}: WARNING ⚠️ (diff={diff:.2e})")

            failed_features.append(col)
            all_ok = False

    # --------------------------------------------------------
    # Extra columns
    # --------------------------------------------------------
    if extra_cols:
        all_ok = False
        failed_features.extend(extra_cols)

        if verbose:
            print("\nUnexpected columns in stored features:")
            for col in extra_cols:
                print(f" - {col}")

    # --------------------------------------------------------
    # Missing columns
    # --------------------------------------------------------
    if missing_cols:
        all_ok = False
        failed_features.extend(missing_cols)

        if verbose:
            print("\nMissing columns in stored features:")
            for col in missing_cols:
                print(f" - {col}")

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------
    status = "PASS" if all_ok else "WARNING"

    if verbose:
        print(f"\n=== RESULT: {status} ===")

    return {
        "status": status,
        "n_issues": len(failed_features),
        "failed_features": sorted(set(failed_features)),
    }