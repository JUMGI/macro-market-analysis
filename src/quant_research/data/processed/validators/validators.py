from quant_research.data.processed.config.config import EXPECTED_COLUMNS


def validate_expected_columns(df, asset: str) -> list:
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]

    if missing_cols:
        print(f"⚠ {asset} missing columns: {missing_cols}")

    return missing_cols