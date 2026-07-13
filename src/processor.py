from __future__ import annotations

import pandas as pd


def build_output_dataframe(df: pd.DataFrame, output_columns: list[dict[str, str]], plan_id: str, plan_type_label: str, precision: int) -> pd.DataFrame:
    data: dict[str, object] = {}
    for column in output_columns:
        name = column["name"]
        source = column["source"]
        if source == "plan_id":
            data[name] = plan_id
        elif source == "plan_type_label":
            data[name] = plan_type_label
        elif source == "Number":
            data[name] = df[source].astype(str)
        else:
            data[name] = pd.to_numeric(df[source], errors="raise")
    return pd.DataFrame(data)
