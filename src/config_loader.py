from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProjectConfig:
    root_dir: Path
    data: dict[str, Any]

    @property
    def input_root(self) -> Path:
        return self.root_dir / self.data["paths"]["input_root"]

    @property
    def output_root(self) -> Path:
        return self.root_dir / self.data["paths"]["output_root"]

    @property
    def logs_root(self) -> Path:
        return self.root_dir / self.data["paths"]["logs_root"]


def load_config(config_path: Path) -> ProjectConfig:
    with config_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    for key in ["paths", "input", "output", "id_rules", "plan_type_labels", "required_input_columns", "output_columns"]:
        if key not in data:
            raise ValueError(f"Config sem chave obrigatoria: {key}")

    for key in ["input_root", "output_root", "logs_root"]:
        if key not in data["paths"]:
            raise ValueError(f"Config.paths sem chave obrigatoria: {key}")

    root_dir = config_path.resolve().parent
    return ProjectConfig(root_dir=root_dir, data=data)
