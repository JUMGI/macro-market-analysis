from collections import defaultdict
from typing import Dict, List
import warnings

from quant_research.research.feature_selection.groups.group_registry import GROUP_REGISTRY


def infer_input_type(feature_info: dict) -> str:
    inputs = feature_info.get("inputs", [])

    if any("_Z" in x for x in inputs):
        return "normalized"

    return "raw"


class FeatureGrouper:

    def group(self, feature_info: Dict[str, dict]) -> Dict[str, List[str]]:

        groups = defaultdict(list)
        unmapped = []

        for feature_name, info in feature_info.items():

            context = {
                "input_type": infer_input_type(info)
            }

            matched = False

            for group_def in GROUP_REGISTRY:

                if group_def.matches(info, context):
                    groups[group_def.name].append(feature_name)
                    matched = True
                    break

            if not matched:
                groups["other"].append(feature_name)
                unmapped.append((feature_name, context, info))

        # 🔥 WARNING CENTRALIZADO
        if unmapped:
            msg = "\n".join(
                [
                    f"{f} | context={c} | measure={i.get('measure')} operator={i.get('operator')} transform={i.get('transform')}"
                    for f, c, i in unmapped
                ]
            )

            warnings.warn(
                f"\n⚠️ Unmapped features detected (update GROUP_REGISTRY):\n{msg}\n",
                UserWarning
            )

        return dict(groups)