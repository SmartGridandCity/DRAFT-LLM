"""
Shared I/O utilities for Support Protocol 2.
"""

from typing import Dict, Any, Union
from pathlib import Path

import pandas as pd
import yaml


def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    """Load a YAML file into a dictionary."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_table(data_root: Path, relative_path: str) -> pd.DataFrame:
    """
    Load a table from a relative path under data_root.

    Supports common formats: Parquet, CSV, Feather.
    """
    full_path = data_root / relative_path
    if not full_path.is_file():
        raise FileNotFoundError(f"Table not found: {full_path}")

    suffix = full_path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(full_path)
    elif suffix in [".csv", ".tsv"]:
        sep = "," if suffix == ".csv" else "\t"
        return pd.read_csv(full_path, sep=sep)
    elif suffix in [".feather", ".ft"]:
        return pd.read_feather(full_path)
    else:
        raise ValueError(f"Unsupported table format: {suffix} at {full_path}")


def load_main_table(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Load the main analysis table according to the SP2 config.
    """
    data_root = Path(config.get("data_root", "."))
    main_cfg = config.get("main_table", {})
    path = main_cfg.get("path")
    if not path:
        raise ValueError("Config must specify main_table.path.")
    return load_table(data_root, path)


def summarize_schema(dataset_card: Dict[str, Any], config: Dict[str, Any], df_main) -> Dict[str, Any]:
    """
    Create a lightweight schema summary based on:
    - dataset card variables,
    - main table shape,
    - declared modalities in config.
    """
    variables = dataset_card.get("variables", [])
    variable_roles = {v["name"]: v.get("role", "feature") for v in variables if "name" in v}

    modalities_cfg = config.get("modalities", {})
    active_modalities = {
        k: bool(v.get("enabled", (k == "tabular")))
        for k, v in modalities_cfg.items()
    }

    summary = {
        "main_table": {
            "n_rows": int(df_main.shape[0]),
            "n_columns": int(df_main.shape[1]),
        },
        "variables": {
            "n_total": int(len(variable_roles)),
            "by_role": {},
        },
        "modalities": active_modalities,
    }

    # Count by role
    role_counts = {}
    for name, role in variable_roles.items():
        role_counts[role] = role_counts.get(role, 0) + 1
    summary["variables"]["by_role"] = role_counts

    return summary
