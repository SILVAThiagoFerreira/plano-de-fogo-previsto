from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_input_dataframe(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"CSV sem colunas obrigatórias: {missing}")

    if "Number" in df.columns:
        numbers = pd.to_numeric(df["Number"], errors="coerce")
        invalid_mask = numbers.isna() | (numbers <= 0) | (numbers % 1 != 0)
        if invalid_mask.any():
            invalid_values = df.loc[invalid_mask, "Number"].tolist()
            raise ValueError(f"Coluna Number invalida. Valores esperados: inteiros positivos. Encontrados: {invalid_values}")


def validate_output_schema(columns: list[str], required_columns: list[str]) -> None:
    if columns != required_columns:
        raise ValueError(f"Schema de saída inválido. Esperado={required_columns} Obtido={columns}")


def validate_output_target(output_file: Path) -> None:
    if output_file.suffix.lower() != ".xlsx":
        raise ValueError(f"Saída inválida: {output_file}")
