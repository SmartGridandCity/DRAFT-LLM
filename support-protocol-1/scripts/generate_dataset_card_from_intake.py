#!/usr/bin/env python
"""
Generate a skeleton dataset card JSON from a simple intake CSV.

This is intentionally minimal: it maps high-level intake fields into
the dataset card structure and leaves lists (variables, outcomes, etc.)
for the user to complete manually.

Usage:
    python scripts/generate_dataset_card_from_intake.py \
        --intake my_study_intake.csv \
        --output my_study_dataset_card.json
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict


def parse_intake_csv(path: Path) -> Dict[str, Dict[str, str]]:
    """
    Parse intake CSV into a dict: section -> {field_name: example_value}.
    """
    sections: Dict[str, Dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            section = row["section"].strip()
            field = row["field_name"].strip()
            value = (row.get("example_value") or "").strip()
            sections.setdefault(section, {})[field] = value
    return sections


def main():
    parser = argparse.ArgumentParser(description="Generate dataset card skeleton from intake form.")
    parser.add_argument("--intake", type=Path, required=True, help="Path to intake CSV.")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON path for dataset card.")
    args = parser.parse_args()

    sections = parse_intake_csv(args.intake)

    # Minimal skeleton; many fields intentionally left empty for manual fill-in.
    card = {
        "card_metadata": {
            "card_id": sections.get("card_metadata", {}).get("card_id", ""),
            "version": sections.get("card_metadata", {}).get("version", "0.1.0"),
            "last_updated": sections.get("card_metadata", {}).get("last_updated", ""),
            "prepared_by": sections.get("card_metadata", {}).get("prepared_by", ""),
            "approved_by": sections.get("card_metadata", {}).get("approved_by", ""),
            "data_freeze_date": sections.get("card_metadata", {}).get("data_freeze_date", ""),
            "notes": ""
        },
        "study_overview": {
            "title": sections.get("study_overview", {}).get("title", ""),
            "primary_question": sections.get("study_overview", {}).get("primary_question", ""),
            "intended_use": sections.get("study_overview", {}).get("intended_use", "exploratory"),
            "intended_use_details": sections.get("study_overview", {}).get("intended_use_details", ""),
            "task_types": [
                t.strip() for t in sections.get("study_overview", {}).get("task_types", "").split(",") if t.strip()
            ] or ["other"],
            "secondary_endpoints": [
                e.strip() for e in sections.get("study_overview", {}).get("secondary_endpoints", "").split(";") if e.strip()
            ],
            "regulatory_context": sections.get("study_overview", {}).get("regulatory_context", "")
        },
        "cohort": {
            "inclusion_criteria": [
                c.strip() for c in sections.get("cohort", {}).get("inclusion_criteria", "").split(";") if c.strip()
            ],
            "exclusion_criteria": [
                c.strip() for c in sections.get("cohort", {}).get("exclusion_criteria", "").split(";") if c.strip()
            ],
            "time_origin": sections.get("cohort", {}).get("time_origin", ""),
            "cohort_size_estimate": int(sections.get("cohort", {}).get("cohort_size_estimate", "0") or 0),
            "multi_dataset_roles": []
        },
        "data_sources": [],
        "variables": [],
        "outcomes": [],
        "sensitive_attributes": [],
        "constraints_and_priorities": {
            "expected_sample_size": int(
                sections.get("constraints_and_priorities", {}).get("expected_sample_size", "0") or 0
            ),
            "approx_feature_dimensionality": int(
                sections.get("constraints_and_priorities", {}).get("approx_feature_dimensionality", "0") or 0
            ),
            "compute_environment": sections.get("constraints_and_priorities", {}).get(
                "compute_environment", "workstation"
            ),
            "access_limitations": sections.get("constraints_and_priorities", {}).get(
                "access_limitations", ""
            ),
            "analysis_priorities": [
                p.strip()
                for p in sections.get("constraints_and_priorities", {})
                .get("analysis_priorities", "")
                .split(",")
                if p.strip()
            ],
            "required_metrics": [
                m.strip()
                for m in sections.get("constraints_and_priorities", {})
                .get("required_metrics", "")
                .split(",")
                if m.strip()
            ],
            "forbidden_operations": [
                o.strip()
                for o in sections.get("constraints_and_priorities", {})
                .get("forbidden_operations", "")
                .split(",")
                if o.strip()
            ],
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(card, f, indent=2)
    print(f"Wrote skeleton dataset card to {args.output}")


if __name__ == "__main__":
    main()
