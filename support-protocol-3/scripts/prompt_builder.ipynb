"""
Prompt builder for Support Protocol 3.

Given a fully constructed configuration dictionary, this module:

- Builds a concrete base system prompt string.
- Provides a small set of user prompt templates.

The structure of the prompts follows the description in Support Protocol 3.
"""

from __future__ import annotations

from typing import Any, Dict


def build_base_system_prompt(config: Dict[str, Any]) -> str:
    """Instantiate the base system prompt from the configuration."""
    study = config.get("study_profile", {})
    user = config.get("user_profile", {})
    gov = config.get("governance", {})
    flags = config.get("data_risk_flags", {})

    sensitive = ", ".join(gov.get("sensitive_attributes", [])) or "none"
    allowed_uses = ", ".join(gov.get("allowed_uses", [])) or "not specified"
    privacy_rules = ", ".join(gov.get("privacy_rules", [])) or "none"
    forbidden_ops = ", ".join(gov.get("forbidden_operations", [])) or "none"

    # Shallow pretty-print of risk flags
    risk_flag_pairs = ", ".join(
        f"{k}={v}" for k, v in flags.items()
    ) or "none"

    return f"""You are a data analysis assistant configured for this specific study.

Study profile
- Goal: {study.get('goal', 'unspecified')}
- Analysis type: {study.get('analysis_type', 'unspecified')}
- Intended use: {study.get('intended_use', 'unspecified')}

User profile
- Expertise: {user.get('expertise', 'unspecified')}
- Programming language: {user.get('language', 'unspecified')}
- Interaction style: {user.get('interaction_style', 'unspecified')}
- Code style: {user.get('code_style', 'unspecified')}

Governance and safety
- Sensitive attributes: {sensitive}
- Allowed uses: {allowed_uses}
- Privacy rules: {privacy_rules}
- Forbidden operations: {forbidden_ops}
- Interpretability requirements: {", ".join(gov.get("interpretability_requirements", [])) or "none"}

Data-driven cues (from statistics card)
- Key risk/complexity flags: {risk_flag_pairs}

Behavioral requirements
- Ground all proposals in the dataset card (SP0) and statistics card (SP1), as summarized in this configuration.
- Respect all governance, privacy, and resource constraints.
- Prioritize interpretable, resource-appropriate methods.
- Explicitly discuss flagged risks (e.g., imbalance, missingness, heterogeneity) whenever they are relevant.
"""


def build_user_prompt_templates(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Build short user prompt templates, parameterized by the configuration
    but still generic enough for reuse across multiple queries.
    """
    study = config.get("study_profile", {})
    goal = study.get("goal", "the current study")
    analysis_type = study.get("analysis_type", "predictive")

    eda = (
        "Using the current configuration, propose an initial exploratory data analysis "
        f"(EDA) plan for {goal} in this {analysis_type} setting. "
        "Explicitly reference any data risk flags (e.g., imbalance, missingness, heterogeneity) "
        "and suggest checks that align with the stated governance and resource constraints."
    )

    modeling = (
        "Propose baseline and candidate models consistent with the configuration, including "
        "preprocessing steps and evaluation strategies. Your suggestions should:\n"
        "- Respect the declared study goal and intended use.\n"
        "- Align with the user's expertise and preferred programming language.\n"
        "- Account for the data risk flags (e.g., outcome imbalance, small subgroups).\n"
        "- Stay within the allowed libraries and compute budget."
    )

    robustness = (
        "Describe robustness checks and diagnostics appropriate for this study, given the "
        "configuration and the statistics card. Cover aspects such as:\n"
        "- Overfitting and generalization (e.g., resampling, permutation tests).\n"
        "- Fairness and subgroup performance, especially along sensitive attributes.\n"
        "- Stability of key features or patterns.\n"
        "Explain how each proposed check relates to the dataset's empirical properties."
    )

    return {
        "eda": eda,
        "modeling": modeling,
        "robustness": robustness,
    }
