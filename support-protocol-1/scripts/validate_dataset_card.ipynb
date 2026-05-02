#!/usr/bin/env python
"""
Validate a dataset card JSON file against the canonical JSON Schema.

Usage:
    python scripts/validate_dataset_card.py \
        --card examples/dataset_card_simple.json \
        --schema schema/dataset_card.schema.json
"""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Validate a DRAFT-LLM dataset card.")
    parser.add_argument(
        "--card", type=Path, required=True, help="Path to dataset card JSON file."
    )
    parser.add_argument(
        "--schema",
        type=Path,
        required=True,
        help="Path to JSON Schema for dataset cards.",
    )
    args = parser.parse_args()

    card = load_json(args.card)
    schema = load_json(args.schema)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(card), key=lambda e: e.path)

    if not errors:
        print(f"OK: {args.card} is valid against {args.schema}.")
        sys.exit(0)

    print(f"ERROR: {len(errors)} validation error(s) found in {args.card}:")
    for err in errors:
        loc = "/".join(str(x) for x in err.path) or "(root)"
        print(f" - Path: {loc}")
        print(f"   Message: {err.message}")
    sys.exit(1)


if __name__ == "__main__":
    main()
