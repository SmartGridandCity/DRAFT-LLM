"""
Tabular statistics and diagnostics for Support Protocol 2.

Implements:
- Global tabular statistics:
  - sample size, number of features, number of outcomes,
  - missingness per column, outcome distribution, numeric and categorical summaries,
  - group-wise outcome rates for sensitive attributes.
- Advanced diagnostics:
  - correlations, PCA, mutual information, surrogate feature importances.
"""

from typing import Dict, Any, List

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mutual_info_score


def _get_variable_roles(dataset_card: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract a {column_name: role} mapping from the dataset card.

    The expected structure is:
    dataset_card["variables"] = [
        {"name": "col1", "role": "feature"},
        {"name": "outcome", "role": "outcome"},
        ...
    ]
    """
    variables = dataset_card.get("variables", [])
    return {v["name"]: v.get("role", "feature") for v in variables if "name" in v}


def build_tabular_datamart(df: pd.DataFrame, dataset_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute global and advanced statistics for mixed (numeric + categorical) tabular data.

    Parameters
    ----------
    df : pd.DataFrame
        Main analysis table with one row per entity (subject/episode/etc.).
    dataset_card : dict
        Dataset card from Support Protocol 1.

    Returns
    -------
    dict
        A dictionary suitable for inclusion under eda_datamarts["tabular"].
    """
    variable_roles = _get_variable_roles(dataset_card)

    target_cols: List[str] = [c for c, r in variable_roles.items() if r == "outcome"]
    sensitive_cols: List[str] = [c for c, r in variable_roles.items() if r == "sensitive"]

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "string", "bool"]).columns.tolist()

    # Global sizes
    n_rows = int(df.shape[0])
    n_features = int(len([c for c, r in variable_roles.items() if r == "feature"]))
    n_outcomes = int(len(target_cols))

    # Missingness per column
    missing_per_col = df.isna().mean().to_dict()

    # Outcome distributions
    outcome_dist = {}
    for col in target_cols:
        vc = df[col].value_counts(normalize=True, dropna=False)
        outcome_dist[col] = {str(k): float(v) for k, v in vc.items()}

    # Numeric summaries
    if numeric_cols:
        numeric_summary = (
            df[numeric_cols]
            .describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99])
            .to_dict()
        )
    else:
        numeric_summary = {}

    # Categorical summaries (including entropy approximation)
    cat_summary: Dict[str, Any] = {}
    for col in cat_cols:
        s = df[col].astype("object")
        counts = s.value_counts(dropna=False)
        total = len(s)
        probs = counts / total
        # avoid log2(0) by replacing 0 with 1 inside log
        entropy = float(-(probs * np.log2(probs.replace(0, 1))).sum())
        cat_summary[col] = {
            "n_unique": int(s.nunique(dropna=True)),
            "top_values": {str(k): int(v) for k, v in counts.head(5).items()},
            "missing_rate": float(s.isna().mean()),
            "entropy_approx": entropy,
        }

    # Group-wise outcome distributions by sensitive attributes
    group_outcomes: Dict[str, Any] = {}
    if sensitive_cols and target_cols:
        primary_target = target_cols[0]
        for s_col in sensitive_cols:
            try:
                grouped = (
                    df.groupby(s_col)[primary_target]
                    .value_counts(normalize=True, dropna=False)
                    .unstack(fill_value=0)
                )
                # Convert to nested dict: {sensitive_value: {target_value: prob}}
                group_outcomes[s_col] = {
                    str(idx): {str(k): float(v) for k, v in row.items()}
                    for idx, row in grouped.to_dict(orient="index").items()
                }
            except Exception:
                # Fail-soft in case of incompatible types
                continue

    # Correlation matrix for numeric variables
    correlations = {}
    if len(numeric_cols) > 1:
        corr_df = df[numeric_cols].corr()
        correlations = corr_df.to_dict()
    else:
        correlations = {}

    # PCA summary: explained variance on numeric features
    pca_summary = {}
    if len(numeric_cols) > 1:
        # Drop rows with any NaNs in numeric columns for PCA
        clean_numeric = df[numeric_cols].dropna()
        if clean_numeric.shape[0] > 0:
            n_components = min(10, clean_numeric.shape[1])
            pca = PCA(n_components=n_components, random_state=42)
            pca.fit(clean_numeric)
            pca_summary = {
                "n_components": int(n_components),
                "explained_variance_ratio": [float(x) for x in pca.explained_variance_ratio_],
            }

    # Mutual information between features and primary outcome (if discrete)
    mi_scores = {}
    if target_cols:
        y = df[target_cols[0]]
        # We only compute MI if the outcome is discrete
        if y.nunique(dropna=True) <= 50:
            for col in numeric_cols + cat_cols:
                try:
                    x = df[col]
                    # Make simple discretization for numeric features
                    if col in numeric_cols:
                        x = pd.qcut(x, q=10, duplicates="drop")
                    valid = ~(x.isna() | y.isna())
                    if valid.sum() > 0:
                        mi_scores[col] = float(
                            mutual_info_score(x[valid].astype("category"), y[valid].astype("category"))
                        )
                except Exception:
                    continue

    # Surrogate feature importances via RandomForest
    feature_importances = {}
    if target_cols:
        y = df[target_cols[0]]
        features = [c for c, r in variable_roles.items() if r == "feature" and c in df.columns]
        if features:
            X = df[features]
            # Simple encoding: fill NaNs and one-hot encode categoricals
            X_enc = pd.get_dummies(X, dummy_na=True)
            X_enc = X_enc.fillna(0)
            # Use only rows without missing target
            mask = ~y.isna()
            X_enc = X_enc.loc[mask]
            y_non_null = y.loc[mask]

            try:
                if y_non_null.nunique(dropna=True) <= 20:
                    model = RandomForestClassifier(
                        n_estimators=100, random_state=42, n_jobs=-1
                    )
                else:
                    model = RandomForestRegressor(
                        n_estimators=100, random_state=42, n_jobs=-1
                    )
                model.fit(X_enc, y_non_null)
                importances = model.feature_importances_
                feature_importances = {
                    feature: float(imp) for feature, imp in zip(X_enc.columns, importances)
                }
            except Exception:
                feature_importances = {}

    return {
        "n_rows": n_rows,
        "n_features": n_features,
        "n_outcomes": n_outcomes,
        "missing_per_col": {str(k): float(v) for k, v in missing_per_col.items()},
        "numeric_summary": numeric_summary,
        "categorical_summary": cat_summary,
        "outcome_dist": outcome_dist,
        "group_outcomes": group_outcomes,
        "correlations": correlations,
        "pca": pca_summary,
        "mutual_information": mi_scores,
        "feature_importances": feature_importances,
    }
