# EDA Prompt Templates for Support Protocol 2

This file contains prompt templates for DRAFT‑LLM that consume both:
- the **dataset card** (Support Protocol 1), and
- the **statistics card** (Support Protocol 2).

The idea is:
1. Pre-fill these templates with:
   - high-level task metadata from the dataset card, and
   - global / advanced statistics from the statistics card.
2. Send the filled prompt to an LLM to:
   - design an EDA workflow,
   - propose code snippets,
   - recommend preprocessing and modeling strategies aligned with the diagnostics.

Placeholders are written as `{{LIKE_THIS}}` and should be filled using the JSON objects.

---

## 1. Generic blueprint

Use this skeleton to build modality-specific prompts.

> You are an expert in {{MODALITY}} EDA and modeling.
>
> Dataset card (Support Protocol 1):
> - Task: {{TASK_DESCRIPTION}}
> - Outcome(s): {{OUTCOMES}}
> - Sensitive attributes: {{SENSITIVE_ATTRIBUTES}}
> - Technical variables: {{TECHNICAL_VARIABLES}}
>
> Statistics card (Support Protocol 2):
> - Global stats: {{GLOBAL_STATS_SNIPPET}}
> - Advanced diagnostics: {{ADVANCED_STATS_SNIPPET}}
>
> Using this information:
> 1. Propose an EDA workflow (concise bullet list) that:
>    - explicitly uses the diagnostics above, and
>    - is feasible for a data science team using Python.
> 2. Provide Python code (pandas / numpy / matplotlib / scikit-learn / etc.) for:
>    - a few representative diagnostic plots, and
>    - any simple metrics or tables that illustrate data issues.
> 3. Explain how these diagnostics should guide:
>    - choice of model families,
>    - preprocessing / feature engineering,
>    - key hyperparameter ranges or regularization strategies.
>
> Be explicit about which parts of the statistics card you are using in which recommendation.

---

## 2. Tabular EDA prompt

```text
You are an expert in tabular data EDA and predictive modeling.

Dataset card:
- Task: {{TASK_DESCRIPTION}}
- Primary outcome: {{PRIMARY_OUTCOME}} (type: {{OUTCOME_TYPE}})
- Sensitive attributes: {{SENSITIVE_ATTRIBUTES}}
- Technical variables: {{TECHNICAL_VARIABLES}}

Statistics card – tabular datamart:
- Sample size and features: {{N_ROWS}} rows, {{N_FEATURES}} feature columns, {{N_OUTCOMES}} outcome(s).
- Missingness per column: {{MISSING_PER_COL_SUMMARY}}
- Outcome distribution (imbalance): {{OUTCOME_DIST_SUMMARY}}
- Numeric summaries (selected): {{NUMERIC_SUMMARY_SNIPPET}}
- Categorical summaries (selected): {{CATEGORICAL_SUMMARY_SNIPPET}}
- Group-wise outcome rates by sensitive attributes: {{GROUP_OUTCOMES_SNIPPET}}
- Correlation and PCA summaries: {{CORRELATION_PCA_SNIPPET}}
- Mutual information and feature importances: {{MI_IMPORTANCE_SNIPPET}}

Using this information:
1. Propose a concrete EDA workflow (max 12 bullets) that:
   - prioritizes checking outcome imbalance and its relationship with sensitive attributes,
   - identifies problematic missingness or outliers,
   - uses correlations/PCA to understand redundancy and dimensionality,
   - interprets mutual information / feature importances as a rough guide to signal strength.
2. Provide Python code (pandas, matplotlib/seaborn, scikit-learn) to:
   - visualize outcome imbalance overall and by sensitive group,
   - plot missingness patterns for top-{{K}} variables,
   - show a correlation heatmap and a simple PCA scree plot,
   - tabulate top features by feature importance.
3. Explain how these diagnostics should inform:
   - decisions about resampling or class weighting,
   - which features might need transformation or interaction terms,
   - reasonable ranges for regularization strength and tree depth (if using tree-based models).

Keep the code modular and assume `df` is a pandas DataFrame with columns as in the dataset card.

3. Time series EDA prompt
You are an expert in time series EDA and forecasting.

Dataset card:
- Task: short-term forecasting of {{TARGET_SERIES}} with horizon {{HORIZON_DESCRIPTION}}.
- Frequency and span: {{FREQUENCY}}, from {{START_DATE}} to {{END_DATE}}.
- Entity-level metadata (if any): {{ENTITY_METADATA_SNIPPET}}

Statistics card – time series datamart:
- Number of distinct series: {{N_SERIES}}
- Series length summary: {{SERIES_LENGTH_SUMMARY}}
- Series missingness summary: {{SERIES_MISSINGNESS_SUMMARY}}
- Outlier summary: {{OUTLIER_SUMMARY}}
- ACF-based stationarity/seasonality indicators (if available): {{ACF_STATIONARITY_SUMMARY}}

Using this information:
1. Propose an EDA workflow (plots + tests) to understand:
   - regime shifts and change points,
   - seasonality (daily/weekly/etc.),
   - non-stationarity and heterogeneity across series.
2. Provide Python code (pandas, matplotlib, and optionally statsmodels) for:
   - plotting a few representative series, including missingness markers and outliers,
   - visualizing distribution of series lengths and missingness,
   - computing and plotting ACF/PACF for representative series.
3. Explain how these diagnostics should guide:
   - choice of forecasting model families (e.g., classical ARIMA/ETS vs deep sequence models),
   - normalization strategy (per-series vs global),
   - reasonable ranges for look-back windows and forecast horizons.

Assume the time series data is in a long format with columns:
- `entity_id`, `timestamp`, `value`, and possibly a `series_id` column distinguishing multiple series per entity.

4. Image / video EDA prompt
You are an expert in image/video EDA and representation learning.

Dataset card:
- Task: {{IMAGE_TASK_DESCRIPTION}} (e.g., real vs synthetic classification, object recognition).
- Labels: {{LABELS_SUMMARY}}
- Sensitive attributes (if any): {{IMAGE_SENSITIVE_ATTRIBUTES}}

Statistics card – image datamart:
- Number of images/videos: {{N_ITEMS}}
- Label distribution: {{LABEL_DISTRIBUTION}}
- Resolution and aspect ratio statistics: {{RESOLUTION_STATS_SNIPPET}}
- Entropy diagnostics (mean ± std):
  - Global intensity entropy: {{H_GLOBAL_SUMMARY}}
  - Local patch entropy: {{H_LOCAL_SUMMARY}}
  - Spectral entropy: {{H_SPECTRAL_SUMMARY}}

Using this information:
1. Propose an EDA plan to:
   - visualize representative samples per label and per entropy level (e.g., low, medium, high entropy),
   - inspect how entropy and spectral characteristics differ across labels or real vs synthetic data,
   - identify potential artifacts (e.g., strong resizing, compression, or scanner/site effects).
2. Provide Python code (using matplotlib and either Pillow, OpenCV, or scikit-image) to:
   - plot entropy distributions and example images at different entropy levels,
   - compute and display simple montage plots stratified by label and entropy quantiles.
3. Suggest an image/video preprocessing and feature pipeline that leverages these diagnostics, including:
   - choice of resize strategy and interpolation method,
   - patch size for local entropy and/or local feature extraction,
   - a few reasonable default hyperparameter ranges (e.g., image size, number of scales, data augmentation strength).

Assume you have:
- an image metadata DataFrame with file paths and labels,
- entropy summaries similar to those computed in Support Protocol 2.

5. Text EDA prompt
You are an expert in text EDA and NLP.

Dataset card:
- Task: {{TEXT_TASK_DESCRIPTION}} (e.g., document classification, sequence labeling).
- Target: {{OUTCOME_DESCRIPTION}}.
- Language(s) and domain: {{LANG_DOMAIN_DESCRIPTION}}.
- Sensitive attributes (if any): {{TEXT_SENSITIVE_ATTRIBUTES}}.

Statistics card – text datamart:
- Number of documents: {{N_DOCS}}
- Document length stats (tokens per document): {{LENGTH_STATS}}
- Vocabulary summary:
  - Vocab size: {{VOCAB_SIZE}}
  - Top terms: {{TOP_TERMS_SNIPPET}}
- Lexical richness indicators:
  - Type-token ratio: {{TTR}}
  - Approximate Zipf log–log slope: {{ZIPF_SLOPE}}
- Label-specific term usage (if available): {{LABEL_TERM_USAGE_SNIPPET}}

Using this information:
1. Design a text-specific EDA plan (max 10 bullets) that:
   - highlights potential class imbalance in text length and vocabulary,
   - checks for domain drift or rare-domain subgroups,
   - identifies potentially sensitive or identifying terms.
2. Provide Python code (using pandas, matplotlib and a simple tokenizer or vectorizer) to:
   - visualize length distributions overall and by label,
   - inspect class-specific term usage (e.g., via top-n word bar plots),
   - compute and visualize a 2D projection of document embeddings colored by label (you may assume a generic sentence embedding model is available).
3. Explain how these diagnostics should guide:
   - tokenization and truncation choices,
   - selection of model families (e.g., linear models on bag-of-words vs transformer encoders),
   - regularization and max sequence length settings, especially when there is a long-tail of document lengths.

Assume that `df_text` is a pandas DataFrame with `text` and (optionally) `label` columns, and that the statistics above have already been computed.