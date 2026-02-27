# Support Protocol 2 – Dataset Structure and Advanced Summary Statistics for LLM Context

This directory contains the **non-paper assets** for:

> **SUPPORT PROTOCOL 2 – Dataset Structure and Advanced Summary Statistics for LLM Context**

The goal of Support Protocol 2 (SP2) is to build:

1. **Modality-specific EDA datamarts** (tabular, time series, image/video, text, graph).
2. A consolidated **statistics card** (`statistics_card.json`) that summarizes:
   - global dataset structure and distributions, and
   - modality-specific complexity diagnostics.

DRAFT‑LLM uses this statistics card together with the **dataset card** from Support Protocol 1 to:
- understand the data pipeline structure (preprocessing → feature extraction → modeling),
- suggest appropriate modeling and preprocessing approaches, and
- tune key hyperparameters (e.g., window sizes, patch sizes, entropy scales, regularization strength).

Implementation details (Python code, JSON schemas, and prompt templates) live here and are referenced from the manuscript as “See Github…”.

---

## Contents

- `config/sp2_config_example.yaml`  
  Example configuration specifying data locations and modality mappings.

- `schema/statistics_card.schema.json`  
  JSON Schema for validating the aggregated statistics card (`statistics_card.json`).

- `scripts/build_statistics_card.py`  
  Orchestrator script that:
  1. Loads a dataset card (from Support Protocol 1).
  2. Loads the SP2 config.
  3. Calls modality-specific statistic functions.
  4. Writes `statistics_card.json`.

- `scripts/tabular_stats.py`  
  Functions to compute global tabular statistics and advanced diagnostics:
  - sample size, missingness, outcome imbalance,
  - basic numeric/categorical summaries,
  - correlation & PCA summaries,
  - mutual information and surrogate feature importance,
  - group-wise outcome rates for sensitive attributes.

- `scripts/timeseries_stats.py`  
  Functions to compute:
  - coverage and missingness per series,
  - simple outlier counts,
  - seasonality and stationarity indicators (summarized).

- `scripts/image_stats.py`  
  Functions to compute:
  - counts and label distributions,
  - resolution/aspect ratio statistics,
  - global, local, and spectral entropy summaries from sampled images.

- `scripts/text_stats.py`  
  Functions to compute:
  - document counts and length distributions,
  - vocabulary and term-frequency summaries,
  - simple lexical richness indicators.

- `scripts/graph_stats.py`  
  Functions to compute graph-level diagnostics:
  - node/edge counts, degree distributions, components,
  - clustering coefficients and simple community indicators.

- `scripts/utils_io.py`  
  Shared I/O utilities for loading tables and generating a light schema summary.

- `examples/dataset_card_example.json`  
  Example dataset card (from Support Protocol 1) that can be used directly with SP2.

- `examples/statistics_card_example.json`  
  Example statistics card generated from the above dataset card.

- `prompts/eda_prompt_templates.md`  
  LLM prompt templates that consume the dataset card + statistics card, for:
  - tabular,
  - time series,
  - image/video,
  - text (and pattern for other modalities).

---

## Dependencies

These scripts assume a Python 3.9+ environment with:

- `pandas`
- `numpy`
- `pyyaml`
- `scikit-learn`
- `matplotlib` (optional, mostly for notebooks)
- `pyarrow` (for Parquet I/O)
- `Pillow` and `scikit-image` (for image diagnostics)
- `networkx` (for graph diagnostics)
- `statsmodels` (optional, for time series ACF/PACF)
- `jsonschema` (optional, for validating statistics cards against the schema)

Install a minimal set with:

```bash
pip install pandas numpy pyyaml scikit-learn pyarrow pillow scikit-image networkx statsmodels jsonschema
