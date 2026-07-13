from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from .config_loader import load_config
from .processor import build_output_dataframe
from .reader import (
    extract_excel_column_map,
    extract_plan_id_from_excel,
    extract_plan_id_from_filename,
    extract_plan_id_from_pdf,
    locate_input_bundle,
    read_csv,
)
from .validator import validate_input_dataframe, validate_output_schema, validate_output_target
from .writer import apply_numeric_format, write_excel


def _setup_logging(logs_root: Path) -> Path:
    logs_root.mkdir(parents=True, exist_ok=True)
    log_file = logs_root / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()])
    return log_file


def _resolve_plan_id(bundle, config, override_plan_id: str | None = None) -> str:
    if override_plan_id:
        return override_plan_id.strip()

    pdf_regex = config.data["id_rules"]["pdf_regex"]
    filename_regex = config.data["id_rules"]["filename_regex"]

    raw_ids: set[str] = set()

    for pdf_file in bundle.pdf_files:
        plan_id = extract_plan_id_from_pdf(pdf_file, pdf_regex)
        if plan_id:
            raw_ids.add(plan_id)

    for excel_file in bundle.excel_files:
        plan_id = extract_plan_id_from_excel(excel_file, filename_regex)
        if plan_id:
            raw_ids.add(plan_id)

    csv_plan_id = extract_plan_id_from_filename(bundle.csv_file, filename_regex)
    if csv_plan_id:
        raw_ids.add(csv_plan_id)

    if len(raw_ids) == 0:
        if config.data["id_rules"]["interactive_fallback"] and sys.stdin.isatty():
            while True:
                value = input("Digite o ID do plano: ").strip()
                if value:
                    return value
        raise ValueError("Nao foi possivel determinar o ID do plano")

    normalized = {id_.lstrip("0") or "0" for id_ in raw_ids}
    if len(normalized) == 1:
        return normalized.pop()
    raise ValueError(f"IDs de plano conflitantes encontrados: {sorted(raw_ids)}")


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PFP Generator")
    parser.add_argument("--config", default="config.json", help="Caminho do arquivo de configuracao")
    parser.add_argument("--plan-id", help="ID do plano informado manualmente")
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    log_file = _setup_logging(config.logs_root)
    logging.info("Log em %s", log_file)

    bundle = locate_input_bundle(
        config.input_root,
        config.data["input"]["csv_pattern"],
        config.data["input"]["pdf_pattern"],
        config.data["input"]["excel_pattern"],
    )
    logging.info("Entrada detectada: tipo=%s pasta=%s csv=%s", bundle.plan_type, bundle.folder, bundle.csv_file.name)

    df = read_csv(bundle.csv_file)
    validate_input_dataframe(df, config.data["required_input_columns"])

    plan_id = _resolve_plan_id(bundle, config, args.plan_id)
    plan_type_label = config.data["plan_type_labels"][bundle.plan_type]

    if bundle.excel_files:
        diameter_map = extract_excel_column_map(bundle.excel_files[0], "ID", "Diameter")
        df = df.copy()
        df["Diameter"] = df["Number"].astype(str).map(diameter_map)
    else:
        raise ValueError("Nao foi possivel extrair o diametro: XLSX auxiliar ausente")

    output_df = build_output_dataframe(
        df=df,
        output_columns=config.data["output_columns"],
        plan_id=plan_id,
        plan_type_label=plan_type_label,
        precision=config.data["output"]["float_precision"],
    )

    required_columns = [column["name"] for column in config.data["output_columns"]]
    validate_output_schema(list(output_df.columns), required_columns)

    output_file = config.output_root / f"{bundle.plan_type}{plan_id}{config.data['output']['file_suffix']}"
    validate_output_target(output_file)

    write_excel(output_df, output_file, config.data["output"]["sheet_name"], config.data["output"]["column_width"])
    apply_numeric_format(
        output_file,
        config.data["output"]["sheet_name"],
        config.data["output"]["float_precision"],
        config.data["output"].get("column_precisions"),
    )

    logging.info("Arquivo gerado: %s", output_file)
    return 0
