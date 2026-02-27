"""
Time series statistics and diagnostics for Support Protocol 2.

This module assumes a "long" time series table with at least:
- an entity/subject identifier,
- a time column,
- a value column (or multiple series via a series_id_column).

The goal is not full modeling, but to compute global and complexity statistics
that help DRAFT‑LLM reason about:
- coverage and missingness,
- outliers,
- seasonality and stationarity.
"""

from typing import Dict, Any

import numpy as np
import pandas as pd
from pathlib import Path

from utils_io import load_table
try:
    from statsmodels.tsa.stattools import acf
except ImportError:  # optional dependency
    acf = None


def build_timeseries_datamart(config: Dict[str, Any], dataset_card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute global and advanced time series statistics.

    Parameters
    ----------
    config : dict
        SP2 configuration YAML parsed into a dictionary.
    dataset_card : dict
        Dataset card from Support Protocol 1 (unused here but kept for symmetry).

    Returns
    -------
    dict
        Statistics suitable for inclusion under eda_datamarts["timeseries"].
    """
    ts_cfg = config.get("modalities", {}).get("timeseries", {})
    data_root = config.get("data_root", ".")
    table_path = ts_cfg.get("table")
    if not table_path:
        raise ValueError("Timeseries modality is enabled but no 'table' path is specified in config.")

    df_ts = load_table(Path(data_root), table_path)

    id_col = ts_cfg.get("id_column", "id")
    time_col = ts_cfg.get("time_column", "timestamp")
    value_col = ts_cfg.get("value_column", "value")
    series_id_col = ts_cfg.get("series_id_column", None)

    if series_id_col is None:
        df_ts["_series_id_internal"] = value_col
        series_id_col = "_series_id_internal"

    # Basic coercions
    if not np.issubdtype(df_ts[time_col].dtype, np.datetime64):
        df_ts[time_col] = pd.to_datetime(df_ts[time_col], errors="coerce")

    # Per-series coverage and missingness
    group_cols = [id_col, series_id_col]
    grouped = df_ts.groupby(group_cols)

    series_lengths = grouped[value_col].size()
    series_missing = grouped[value_col].apply(lambda s: s.isna().mean())
    series_start = grouped[time_col].min()
    series_end = grouped[time_col].max()

    global_stats = {
        "n_series": int(series_lengths.shape[0]),
        "series_length_summary": series_lengths.describe().to_dict(),
        "series_missing_summary": series_missing.describe().to_dict(),
        "time_span_start": str(series_start.min()) if not series_start.empty else None,
        "time_span_end": str(series_end.max()) if not series_end.empty else None,
    }

    # Simple outlier counts (per series) using median +/- 3 * MAD
    def _outlier_count(s: pd.Series) -> int:
        s_clean = s.dropna()
        if s_clean.empty:
            return 0
        median = s_clean.median()
        mad = (s_clean - median).abs().median()
        if mad == 0:
            return 0
        z = (s_clean - median).abs() / (3 * mad)
        return int((z > 1).sum())

    outlier_counts = grouped[value_col].apply(_outlier_count)
    outlier_summary = outlier_counts.describe().to_dict()

    # ACF-based seasonality + stationarity (lightweight summary)
    acf_summary = {}
    if acf is not None:
        sample_series = df_ts.dropna(subset=[value_col]).groupby(series_id_col)[value_col].nth(0)
        if len(sample_series) > 0:
            # use one representative series from each series_id (or a sample of them)
            # here, we approximate by taking first series of the frame after grouping by group_cols
            first_series = df_ts.sort_values(time_col).groupby(group_cols)[value_col].apply(
                lambda s: s.dropna().values[:500]
            )
            acf_values = []
            for arr in first_series:
                if len(arr) > 3:
                    try:
                        acf_vals = acf(arr, nlags=min(20, len(arr) - 1), fft=True)
                        acf_values.append(acf_vals)
                    except Exception:
                        continue
            if acf_values:
                # Take mean absolute ACF across series as very rough summary
                stacked = np.vstack([a[:20] for a in acf_values if len(a) >= 20])
                mean_abs_acf = np.mean(np.abs(stacked), axis=0)
                acf_summary = {
                    "mean_abs_acf_first_20_lags": [float(x) for x in mean_abs_acf]
                }

    return {
        "global_stats": global_stats,
        "outlier_summary": outlier_summary,
        "acf_stationarity_summary": acf_summary,
    }
