import pandas as pd
import json
import hashlib

from quant_research.systemic.config.config_expander import SystemicConfigExpander
from quant_research.systemic.builders.systemic_builder import SystemicBuilder
from quant_research.systemic.metadata.builder import MetadataBuilder


class SystemicOrchestrator:

    def __init__(self, config):
        self.config = config

    def run(self, panel_prepared, output_path):

        # ----------------------------------------
        # 1. EXPAND FEATURES
        # ----------------------------------------
        expander = SystemicConfigExpander(
            self.config["systemic"]["features"]
        )
        features = expander.expand()

        # ----------------------------------------
        # 2. COMPUTE SYSTEMIC
        # ----------------------------------------
        builder = SystemicBuilder(features)
        df = builder.build(panel_prepared)

        if self.config["panel"]["nan_handling"]["final"]["method"] == "dropna":
            df = df.dropna()

        df_z = (df - df.mean()) / df.std()    

        # ----------------------------------------
        # 3. METADATA (SINGLE SOURCE OF TRUTH)
        # ----------------------------------------
        metadata_builder = MetadataBuilder(features)
        feature_metadata = metadata_builder.build()

        metadata = {
            "dataset_hash": self._hash_df(df),
            "panel_hash": self._hash_df(panel_prepared),
            "config_hash": self._hash_config(self.config),

            "n_rows": df.shape[0],
            "n_features": df.shape[1],

            # 🔥 REAL METADATA
            "features": feature_metadata
        }

        # ----------------------------------------
        # 4. EXPORT
        # ----------------------------------------
        self._export(df, df_z, metadata, output_path)

        return df, df_z, metadata

    # ============================================================
    # HELPERS
    # ============================================================

    def _hash_df(self, df: pd.DataFrame) -> str:
        return hashlib.md5(
            pd.util.hash_pandas_object(df, index=True).values
        ).hexdigest()

    def _hash_config(self, config: dict) -> str:
        import hashlib
        import json
        from pathlib import Path

        def normalize(obj):
            if isinstance(obj, Path):
                return str(obj)
            if isinstance(obj, dict):
                return {k: normalize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [normalize(v) for v in obj]
            return obj

        normalized = normalize(config)

        payload = json.dumps(normalized, sort_keys=True).encode()

        return hashlib.md5(payload).hexdigest()

    def _export(self, df, df_z, metadata, output_path):

        from pathlib import Path
        import json

        path = Path(output_path)
        path.mkdir(parents=True, exist_ok=True)

        df.to_parquet(path / "systemic.parquet")
        df_z.to_parquet(path / "systemic_z.parquet")

        with open(path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)