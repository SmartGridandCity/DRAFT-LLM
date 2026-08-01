"""
Main driver for Support Protocol 3:
LLM Configuration Using Structured Form Responses.

Usage (from repository root):

    python -m scripts.build_llm_config \
        --dataset-card path/to/dataset_card.json \
        --statistics-card path/to/statistics_card.json \
        --output-config path/to/llm_config.json

Optional:
    --project-id PROJECT_ID
    --protocol-config config/sp3_config_example.yaml
    --force   # proceed even if blocking consistency errors are detected (not recommended)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from .utils_io import load_json, save_json, load_yaml
from .consistency_checks import cross_check_cards
from .prompt_builder import build_base_system_prompt, build_user_prompt_templates


def derive_data_risk_flags(
    statistics_card: Dict[str, Any],
    cfg: Dict[str, Any] | None = None,
) -> Dict[str, bool]:
    """
    Derive data risk flags from the statistics card and protocol configuration.

    This implementation is intentionally lightweight and modality-agnostic.
    It expects (if available) the following structure in the statistics card:

        {
          "global": { "n_samples": ... },
          "outcomes": {
            "outcome_name": {
              "class_proportions": { "class0": 0.2, "class1": 0.8 }
            }
          },
          "features": {
            "feature_name": {
              "missing_rate": 0.1
            },
            ...
          },
          "heterogeneity": {
            "has_strong_subgroups": true
          }
        }

    All fields are optional; missing fields simply reduce the level
    of automatic flagging.
    """
    risk_cfg = (cfg or {}).get("risk_thresholds", {})
    imb_thresh = float(risk_cfg.get("imbalance_ratio_high", 0.8))
    miss_thresh = float(risk_cfg.get("missingness_rate_high", 0.2))

    flags = {
        "imbalance_flag": False,
        "must_discuss_imbalance": False,
        "missingness_flag": False,
        "must_address_missingness": False,
        "heterogeneity_flag": False,
        "emphasize_heterogeneity": False,
    }

    # Outcome imbalance
    outcomes = statistics_card.get("outcomes", {})
    for outcome_name, info in outcomes.items():
        props = (info or {}).get("class_proportions", {})
        if not props:
            continue
        max_prop = max(props.values())
        if max_prop >= imb_thresh:
            flags["imbalance_flag"] = True
            flags["must_discuss_imbalance"] = True
            break

    # Missingness
    features = statistics_card.get("features", {})
    for feat_name, finfo in features.items():
        mr = (finfo or {}).get("missing_rate", 0.0)
        if mr is not None and mr >= miss_thresh:
            flags["missingness_flag"] = True
            flags["must_address_missingness"] = True
            break

    # Heterogeneity
    hetero = statistics_card.get("heterogeneity", {})
    if hetero.get("has_strong_subgroups"):
        flags["heterogeneity_flag"] = True
        flags["emphasize_heterogeneity"] = True

    return flags


def build_config(
    dataset_card: Dict[str, Any],
    statistics_card: Dict[str, Any],
    protocol_cfg: Dict[str, Any] | None,
    project_id_override: str | None = None,
) -> Dict[str, Any]:
    """Map dataset/statistics cards to an LLM configuration dictionary."""
    protocol_cfg = protocol_cfg or {}
    proj_defaults = protocol_cfg.get("project_defaults", {})
    interaction_defaults = protocol_cfg.get("interaction_defaults", {})
    resources_cfg = protocol_cfg.get("resources", {})
    gov_defaults = protocol_cfg.get("governance_defaults", {})

    # Project ID and versions
    project_id = (
        project_id_override
        or dataset_card.get("project_id")
        or proj_defaults.get("default_project_id", "unnamed_study")
    )
    sp0_version = dataset_card.get("version", "sp0_v0.0")
    sp1_version = statistics_card.get("version", "sp1_v0.0")

    # Study profile
    task = dataset_card.get("task", {})
    study_profile = {
        "goal": task.get("goal", "unspecified"),
        "analysis_type": task.get("analysis_type", "predictive"),
        "intended_use": dataset_card.get(
            "intended_use",
            proj_defaults.get("default_intended_use", "internal_research"),
        ),
        "notes": dataset_card.get("study_notes", ""),
    }

    # User profile
    user_card = dataset_card.get("user_profile", {})
    user_profile = {
        "expertise": user_card.get(
            "expertise", interaction_defaults.get("expertise", "intermediate")
        ),
        "language": user_card.get(
            "language", interaction_defaults.get("language", "python")
        ),
        "interaction_style": user_card.get(
            "interaction_style",
            interaction_defaults.get("interaction_style", "standard_explanations"),
        ),
        "code_style": user_card.get(
            "code_style", interaction_defaults.get("code_style", "focused_examples")
        ),
    }

    # Governance
    gov_card = dataset_card.get("governance", {})
    governance = {
        "sensitive_attributes": gov_card.get("sensitive_attributes", []),
        "allowed_uses": gov_card.get("allowed_uses", []),
        "privacy_rules": gov_card.get(
            "privacy_rules", gov_defaults.get("privacy_rules", [])
        ),
        "forbidden_operations": gov_card.get("forbidden_operations", []),
        "interpretability_requirements": gov_card.get(
            "interpretability_requirements",
            gov_defaults.get("interpretability_requirements", []),
        ),
    }

    # Resources
    resources = {
        "compute_budget": resources_cfg.get("compute_budget", "medium"),
        "allowed_libraries": resources_cfg.get("allowed_libraries", []),
        "environment_constraints": resources_cfg.get(
            "environment_constraints", []
        ),
    }

    # Data risk flags
    data_risk_flags = derive_data_risk_flags(statistics_card, protocol_cfg)

    # Assemble preliminary config without prompts
    config: Dict[str, Any] = {
        "project_id": project_id,
        "sp0_version": sp0_version,
        "sp1_version": sp1_version,
        "study_profile": study_profile,
        "user_profile": user_profile,
        "governance": governance,
        "resources": resources,
        "data_risk_flags": data_risk_flags,
    }

    # Prompts
    base_system_prompt = build_base_system_prompt(config)
    prompt_templates = build_user_prompt_templates(config)

    config["base_system_prompt"] = base_system_prompt
    config["prompt_templates"] = prompt_templates

    return config


def _load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load JSON schema if available; return empty dict on failure."""
    try:
        with schema_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN] Schema file not found: {schema_path}; skipping validation.", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse schema {schema_path}: {e}; skipping validation.", file=sys.stderr)
        return {}


def _validate_config(config: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Optional JSON Schema validation (no-op if jsonschema is not installed or schema is empty)."""
    if not schema:
        return
    try:
        import jsonschema  # type: ignore
    except ImportError:
        print(
            "[WARN] jsonschema library not installed; skipping config validation.",
            file=sys.stderr,
        )
        return

    try:
        jsonschema.validate(instance=config, schema=schema)  # type: ignore[attr-defined]
    except jsonschema.exceptions.ValidationError as e:  # type: ignore[attr-defined]
        print(f"[ERROR] LLM configuration failed schema validation: {e}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build LLM configuration from dataset and statistics cards (Support Protocol 3)."
    )
    parser.add_argument(
        "--dataset-card",
        required=True,
        help="Path to dataset card JSON (Support Protocol 0).",
    )
    parser.add_argument(
        "--statistics-card",
        required=True,
        help="Path to statistics card JSON (Support Protocol 1).",
    )
    parser.add_argument(
        "--output-config",
        required=True,
        help="Path to write the resulting LLM configuration JSON.",
    )
    parser.add_argument(
        "--project-id",
        default=None,
        help="Optional override for project_id in the configuration.",
    )
    parser.add_argument(
        "--protocol-config",
        default=None,
        help="Optional YAML configuration controlling protocol defaults.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Proceed even if blocking consistency errors are detected (NOT recommended).",
    )

    args = parser.parse_args(argv)

    dataset_card = load_json(args.dataset_card)
    statistics_card = load_json(args.statistics_card)
    protocol_cfg = load_yaml(args.protocol_config) if args.protocol_config else None

    # Consistency checks
    warnings, errors = cross_check_cards(dataset_card, statistics_card)

    for w in warnings:
        print(f"[WARN] {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        if not args.force:
            print(
                "[INFO] Blocking errors detected. Resolve them or re-run with --force to override.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Build configuration
    config = build_config(
        dataset_card=dataset_card,
        statistics_card=statistics_card,
        protocol_cfg=protocol_cfg,
        project_id_override=args.project_id,
    )

    # Validate against schema if available
    schema_path = Path(__file__).resolve().parents[1] / "schema" / "llm_config.schema.json"
    schema = _load_schema(schema_path)
    _validate_config(config, schema)

    # Save
    save_json(config, args.output_config)
    print(f"[INFO] LLM configuration written to {args.output_config}")


if __name__ == "__main__":
    main()
