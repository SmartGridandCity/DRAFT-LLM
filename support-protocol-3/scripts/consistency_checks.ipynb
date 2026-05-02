"""
Consistency checks between the dataset card (Support Protocol 0)
and the statistics card (Support Protocol 1).

Implements the feedback loop described in Support Protocol 3:

1. Cross-check key elements.
2. Flag mismatches and prompt revisions.
3. Iterate until alignment.

This module does not perform the loop itself; it provides the
checks and diagnostics that a pipeline or user can act on.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _get(d: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Lightweight helper for nested dict access using dotted paths."""
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def cross_check_cards(
    dataset_card: Dict[str, Any],
    statistics_card: Dict[str, Any],
) -> Tuple[List[str], List[str]]:
    """
    Cross-check key elements between dataset and statistics cards.

    Returns:
        warnings: non-fatal issues that should be reviewed.
        errors: blocking issues that should be resolved before proceeding.
    """
    warnings: List[str] = []
    errors: List[str] = []

    # 1. Outcome variable presence and basic consistency
    outcome_var = _get(dataset_card, "task.outcome_variable")
    if outcome_var is None:
        errors.append(
            "Dataset card: task.outcome_variable is missing; cannot align with statistics card."
        )
    else:
        stats_outcomes = _get(statistics_card, "outcomes", {})
        if outcome_var not in stats_outcomes:
            errors.append(
                f"Outcome variable '{outcome_var}' declared in dataset card "
                "but not summarized in statistics card under 'outcomes'."
            )

    # 2. Record counts
    declared_n = _get(dataset_card, "data_summary.n_samples")
    observed_n = _get(statistics_card, "global.n_samples")
    if declared_n is not None and observed_n is not None:
        if int(declared_n) != int(observed_n):
            errors.append(
                f"Sample count mismatch: dataset card declares {declared_n} samples, "
                f"statistics card reports {observed_n}."
            )
    elif declared_n is None:
        warnings.append(
            "Dataset card: data_summary.n_samples is missing; cannot fully cross-check sample count."
        )
    elif observed_n is None:
        warnings.append(
            "Statistics card: global.n_samples is missing; cannot fully cross-check sample count."
        )

    # 3. Sensitive attributes presence
    sens_attrs = _get(dataset_card, "governance.sensitive_attributes", [])
    if sens_attrs:
        stats_features = _get(statistics_card, "features", {})
        for attr in sens_attrs:
            if attr not in stats_features:
                warnings.append(
                    f"Sensitive attribute '{attr}' is declared in dataset card but "
                    "is not summarized in statistics card under 'features'."
                )

    # 4. Outcome type compatibility (high-level)
    declared_type = _get(dataset_card, "task.outcome_type")
    stats_type = _get(statistics_card, "outcomes_type", None)

    if declared_type and stats_type and declared_type != stats_type:
        warnings.append(
            f"Outcome type mismatch: dataset card declares '{declared_type}', "
            f"statistics card reports '{stats_type}'. Please confirm."
        )

    return warnings, errors
