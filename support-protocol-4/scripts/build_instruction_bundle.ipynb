import argparse
import json
from pathlib import Path
from typing import Any, Dict

from sp4.extractor import load_json, extract_audit_context
from sp4.profiles import build_audit_profiles
from sp4.prompts import load_audit_templates, generate_audit_prompts
from sp4.validate import (
    apply_governance_filters,
    validate_bundle,
    add_metadata_and_timestamp,
)


def _load_user_focus(path: str | Path | None) -> Dict[str, Any]:
    if path is None:
        return {}
    return load_json(path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Support Protocol 4 – Build DRAFT LLM instruction bundle."
    )
    parser.add_argument(
        "--dataset-card", required=True, help="Path to SP0 dataset card JSON."
    )
    parser.add_argument(
        "--statistics-card", required=True, help="Path to SP1 statistics card JSON."
    )
    parser.add_argument(
        "--llm-config", required=True, help="Path to SP2 LLM config JSON."
    )
    parser.add_argument(
        "--audit-templates",
        required=True,
        help="Path to method-agnostic DRAFT audit templates JSON.",
    )
    parser.add_argument(
        "--user-focus",
        default=None,
        help="Optional path to user focus JSON (enabled audits, priorities).",
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="Project identifier to embed in the instruction bundle.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Path to write the resulting instruction bundle JSON.",
    )

    args = parser.parse_args()

    dataset_card = load_json(args.dataset_card)
    statistics_card = load_json(args.statistics_card)
    llm_config = load_json(args.llm_config)
    audit_templates = load_audit_templates(args.audit_templates)
    user_focus = _load_user_focus(args.user_focus)

    # Determine which audits are enabled
    enabled_audits = user_focus.get("enabled_audits")
    if not enabled_audits:
        enabled_audits = ["generalization", "equity", "stability"]

    # Step 1 – Extract audit-relevant parameters
    audit_context, template_context = extract_audit_context(
        dataset_card, statistics_card, llm_config
    )

    # Step 2 – Instantiate audit profiles
    audit_profiles = build_audit_profiles(audit_context, enabled_audits=enabled_audits)

    # Step 3 – Generate audit-specific system and user prompts
    audit_prompts = generate_audit_prompts(
        llm_config=llm_config,
        audit_profiles=audit_profiles,
        audit_templates=audit_templates,
        template_context=template_context,
        enabled_audits=enabled_audits,
    )

    # Build final bundle structure
    bundle: Dict[str, Any] = {"audits": {}}
    for audit_name in enabled_audits:
        if audit_name not in audit_profiles or audit_name not in audit_prompts:
            continue
        bundle["audits"][audit_name] = {
            "system_prompt": audit_prompts[audit_name]["system_prompt"],
            "user_prompt_templates": audit_prompts[audit_name][
                "user_prompt_templates"
            ],
            "profile": audit_profiles[audit_name],
        }

    # Step 4 – Validation and governance checks
    apply_governance_filters(bundle, llm_config.get("governance", {}))
    add_metadata_and_timestamp(
        bundle,
        sp0=dataset_card,
        sp1=statistics_card,
        sp2=llm_config,
        project_id=args.project_id,
    )
    validate_bundle(bundle)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
