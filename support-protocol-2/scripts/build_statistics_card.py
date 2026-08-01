#!/usr/bin/env python
"""
Builds a statistics card for Support Protocol 2.

This script:
1. Loads a dataset card (from Support Protocol 1).
2. Loads a configuration file (sp2_config_example.yaml or similar).
3. Loads the main analysis table and any modality-specific tables.
4. Computes per-modality EDA datamarts.
5. Aggregates these into a single statistics card JSON file.

Usage
-----
python build_statistics_card.py \
  --dataset-card ../support-protocol-1/examples/dataset_card_example.json \
  --config ../support-protocol-2/config/sp2_config_example.yaml \
  --output ../metadata/statistics_card.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from utils_io import load_yaml, load_main_table, summarize_schema
from tabular_stats import build_tabular_datamart
from timeseries_stats import build_timeseries_datamart
from image_stats import build_image_datamart
from text_stats import build_text_datamart
from graph_stats import build_graph_datamart


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build statistics card for Support Protocol 2.")
    parser.add_argument(
        "--dataset-card",
        type=str,
        required=True,
        help="Path to dataset card JSON (from Support Protocol 1).",
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to SP2 configuration YAML (e.g., config/sp2_config_example.yaml).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../metadata/statistics_card.json",
        help="Path to write the output statistics card JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dataset_card_path = Path(args.dataset_card)
    config_path = Path(args.config)
    output_path = Path(args.output)

    if not dataset_card_path.is_file():
        raise FileNotFoundError(f"Dataset card not found: {dataset_card_path}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with dataset_card_path.open("r", encoding="utf-8") as f:
        dataset_card = json.load(f)

    config = load_yaml(config_path)

    # Load main analysis table (tabular base)
    df_main = load_main_table(config)

    eda_datamarts = {}

    # Lightweight schema summary (tables, counts, modalities).
    eda_datamarts["schema"] = summarize_schema(dataset_card, config, df_main)

    modalities_cfg = config.get("modalities", {})

    # Tabular datamart
    if modalities_cfg.get("tabular", {}).get("enabled", True):
        print("[SP2] Computing tabular datamart...")
        eda_datamarts["tabular"] = build_tabular_datamart(df_main, dataset_card)

    # Time series datamart
    if modalities_cfg.get("timeseries", {}).get("enabled", False):
        print("[SP2] Computing time series datamart...")
        eda_datamarts["timeseries"] = build_timeseries_datamart(config, dataset_card)

    # Image datamart
    if modalities_cfg.get("image", {}).get("enabled", False):
        print("[SP2] Computing image datamart...")
        eda_datamarts["image"] = build_image_datamart(config, dataset_card)

    # Text datamart
    if modalities_cfg.get("text", {}).get("enabled", False):
        print("[SP2] Computing text datamart...")
        eda_datamarts["text"] = build_text_datamart(config, dataset_card)

    # Graph datamart
    if modalities_cfg.get("graph", {}).get("enabled", False):
        print("[SP2] Computing graph datamart...")
        eda_datamarts["graph"] = build_graph_datamart(config, dataset_card)

    statistics_card = {
        "dataset_card_id": dataset_card.get("id", "UNKNOWN_DATASET_CARD_ID"),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "eda_datamarts": eda_datamarts,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(statistics_card, f, indent=2)

    print(f"[SP2] Wrote statistics card to {output_path}")


if __name__ == "__main__":
    main()
