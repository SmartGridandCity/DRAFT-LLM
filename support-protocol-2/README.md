# Support Protocol 2 — Dataset Structure and Summary Statistics

**Version:** 1.0  
**Status:** Reference implementation

Support Protocol 2 (SP2) transforms dataset structure and empirical diagnostics into a machine-readable **Statistics Card**.

SP2 consumes the Dataset Card produced by Support Protocol 1, analyzes the configured data modalities, and generates standardized summaries for downstream DRAFT-LLM protocols.

---

## Purpose

While Support Protocol 1 documents the intended study design, SP2 describes the observed structure and characteristics of the available data.

SP2 supports researchers in:

1. summarizing dataset dimensions, variables, and modalities;
2. measuring missingness and outcome imbalance;
3. comparing outcomes across sensitive groups;
4. identifying heterogeneity, dependence, outliers, and structural complexity;
5. computing modality-specific diagnostics;
6. producing a machine-readable Statistics Card; and
7. providing empirical context for downstream audit planning.

These summaries help prevent downstream systems from recommending analyses that are incompatible with the available data.

SP2 performs exploratory diagnostics. It does not train, select, or validate final predictive models.

---

## Directory Structure

```text
support-protocol-2/
├── config/
│   └── sp2_config_example.yaml
├── examples/
│   ├── dataset_card_example.json
│   └── statistics_card_example.json
├── prompts/
│   └── eda_prompt_templates.md
├── schema/
│   └── statistics_card.schema.json
├── scripts/
│   ├── build_statistics_card.py
│   ├── graph_stats.py
│   ├── image_stats.py
│   ├── tabular_stats.py
│   ├── text_stats.py
│   ├── timeseries_stats.py
│   └── utils_io.py
└── README.md
```

---

## Files

### Configuration and schema

#### `config/sp2_config_example.yaml`

Example configuration defining:

- the data root;
- the main analysis table;
- identifier, outcome, and time columns;
- enabled modalities;
- modality-specific data paths; and
- sampling parameters and random seeds.

Copy and adapt this file rather than modifying the reference configuration directly.

#### `schema/statistics_card.schema.json`

Canonical JSON Schema for the Statistics Card.

The schema defines the expected top-level structure and modality-specific sections consumed by downstream DRAFT-LLM components.

---

### Examples

#### `examples/dataset_card_example.json`

Example SP1-compatible Dataset Card used to demonstrate SP2.

#### `examples/statistics_card_example.json`

Example Statistics Card containing tabular summaries and diagnostic results.

---

### Orchestration

#### `scripts/build_statistics_card.py`

Main SP2 orchestration script. It:

1. loads an SP1 Dataset Card;
2. loads the SP2 YAML configuration;
3. loads the main analysis table;
4. determines which modalities are enabled;
5. executes the corresponding modality modules; and
6. writes the aggregated Statistics Card as JSON.

#### `scripts/utils_io.py`

Shared input/output utilities for:

- loading YAML configuration files;
- reading CSV, TSV, Parquet, and Feather tables;
- loading the main analysis table; and
- summarizing dataset schema and variable roles.

---

### Modality-specific diagnostics

#### `scripts/tabular_stats.py`

Computes diagnostics for tabular clinical, biological, or omics data, including:

- dataset dimensions;
- numeric and categorical summaries;
- column-level missingness;
- outcome distributions;
- group-wise outcome distributions;
- correlations;
- principal component summaries;
- mutual information scores; and
- surrogate random-forest feature importances.

Surrogate feature importance is exploratory and should not be interpreted as causal evidence or final model importance.

#### `scripts/timeseries_stats.py`

Computes summaries for longitudinal data represented in long format, including:

- number of series;
- series-length distributions;
- missingness summaries;
- robust outlier counts; and
- autocorrelation-based diagnostics when `statsmodels` is available.

#### `scripts/image_stats.py`

Computes image metadata and entropy-based diagnostics, including:

- image counts;
- label distributions;
- resolution and aspect-ratio summaries;
- global intensity entropy;
- local patch entropy; and
- spectral entropy.

These measures can identify unusual image structure, but they do not independently establish the presence of batch effects, staining differences, or artifacts.

#### `scripts/text_stats.py`

Computes summaries for clinical notes, pathology reports, and other text data, including:

- document counts;
- document-length distributions;
- vocabulary size;
- frequent terms;
- lexical metrics; and
- label-specific term frequencies.

Embedding and topic summaries are currently represented as extension points.

#### `scripts/graph_stats.py`

Computes structural summaries for graph data, including:

- node and edge counts;
- graph density;
- connected-component counts and sizes;
- degree distributions; and
- clustering-coefficient distributions.

---

### LLM integration

#### `prompts/eda_prompt_templates.md`

Contains modality-specific prompt templates that combine:

- study metadata from the SP1 Dataset Card; and
- empirical summaries from the SP2 Statistics Card.

The templates support LLM-assisted EDA planning, diagnostic visualization, preprocessing recommendations, and model-family selection.

Generated recommendations must be reviewed by qualified investigators before use.

---

## Requirements

- Python 3.9 or later
- `pandas`
- `numpy`
- `PyYAML`
- `scikit-learn`
- `pyarrow`
- `Pillow`
- `scikit-image`
- `networkx`
- `statsmodels`
- `jsonschema`

Install the dependencies:

```bash
python -m pip install \
  pandas \
  numpy \
  pyyaml \
  scikit-learn \
  pyarrow \
  pillow \
  scikit-image \
  networkx \
  statsmodels \
  jsonschema
```

For reproducible use, pin exact dependency versions in the repository environment or lockfile.

---

## Supported Data Formats

The shared table loader supports:

| Format | Extension |
|---|---|
| Parquet | `.parquet` |
| CSV | `.csv` |
| Tab-separated values | `.tsv` |
| Feather | `.feather` or `.ft` |

Image files are referenced through an image metadata table.

---

## Quick Start

### 1. Prepare the Dataset Card

SP2 requires a Dataset Card produced and validated through Support Protocol 1.

An example is available at:

```text
examples/dataset_card_example.json
```

### 2. Create an SP2 configuration

Copy the example configuration:

```bash
cp config/sp2_config_example.yaml config/my_sp2_config.yaml
```

Update the configuration with the correct data paths, column names, modalities, and sampling limits.

Example:

```yaml
data_root: "../data"

main_table:
  path: "main.parquet"
  id_column: "patient_id"

modalities:
  tabular:
    enabled: true
    table: "main.parquet"

  timeseries:
    enabled: false

  image:
    enabled: false

  text:
    enabled: false

  graph:
    enabled: false

sampling:
  image_max_samples: 200
  timeseries_max_series: 200
  random_state: 42
```

Paths are interpreted relative to `data_root` unless otherwise specified by the implementation.

### 3. Build the Statistics Card

Run the command from the `support-protocol-2` directory:

```bash
python scripts/build_statistics_card.py \
  --dataset-card examples/dataset_card_example.json \
  --config config/my_sp2_config.yaml \
  --output statistics_card.json
```

A successful run writes the Statistics Card to the requested output path.

Example output:

```text
[SP2] Wrote statistics card to statistics_card.json
```

### 4. Validate the Statistics Card

Validate the generated file against the canonical schema:

```bash
python -m jsonschema \
  -i statistics_card.json \
  schema/statistics_card.schema.json
```

Schema validation confirms structural conformity. It does not verify that the computed statistics are scientifically appropriate or correctly interpreted.

---

## Configuration Reference

### Main analysis table

```yaml
main_table:
  path: "main.parquet"
  id_column: "patient_id"
```

The main table is used to compute the global schema summary and tabular diagnostics.

### Tabular modality

```yaml
tabular:
  enabled: true
  table: "main.parquet"
```

Optional column allowlists and denylists may be added when supported by the implementation.

### Time-series modality

```yaml
timeseries:
  enabled: true
  table: "timeseries.parquet"
  id_column: "patient_id"
  time_column: "timestamp"
  value_column: "value"
  series_id_column: "series_id"
```

The time-series table should use long format.

### Image modality

```yaml
image:
  enabled: true
  metadata_table: "image_metadata.parquet"
  path_column: "path"
  label_column: "label"
  sensitive_columns:
    - "site"
    - "scanner_type"
```

### Text modality

```yaml
text:
  enabled: true
  table: "text.parquet"
  id_column: "patient_id"
  text_column: "note_text"
  label_column: "label"
```

### Graph modality

```yaml
graph:
  enabled: true
  edge_list_path: "graph_edges.csv"
  node_attribute_path: "graph_nodes.csv"
  source_column: "source"
  target_column: "target"
```

---

## Statistics Card Organization

A Statistics Card generally contains:

| Section | Purpose |
|---|---|
| Metadata | Statistics Card identifier, version, and creation information |
| Dataset reference | Association with the source Dataset Card |
| Schema summary | Table dimensions, variable roles, and active modalities |
| Tabular datamart | Missingness, distributions, group outcomes, correlations, PCA, and feature diagnostics |
| Time-series datamart | Coverage, missingness, outliers, and temporal diagnostics |
| Image datamart | Counts, dimensions, labels, and entropy diagnostics |
| Text datamart | Length, vocabulary, lexical, and label-specific summaries |
| Graph datamart | Density, components, degree, and clustering summaries |

The exact field names and constraints are defined in:

```text
schema/statistics_card.schema.json
```

---

## Workflow Integration

The SP2 Statistics Card is combined with the SP1 Dataset Card and passed to subsequent support protocols.

```text
SP1 Dataset Card
        +
Configured data sources
        ↓
SP2 modality diagnostics
        ↓
Statistics Card
        ↓
SP3 LLM configuration
        +
SP4 instruction bundle
        ↓
Generalization, equity, and stability audits
```

SP2 outputs may inform downstream flags such as:

- outcome imbalance requiring explicit discussion;
- insufficient subgroup sample sizes;
- missingness requiring sensitivity analysis;
- site or batch heterogeneity;
- temporal dependence;
- potential leakage;
- high-dimensional feature structure; and
- modality-specific preprocessing requirements.

These flags are diagnostic indicators, not definitive scientific conclusions.

---

## Reproducibility Recommendations

- Preserve the exact SP1 Dataset Card used for each run.
- Version the SP2 configuration file.
- Record the data-freeze date.
- Use stable identifiers for datasets and outputs.
- Set and record the random seed.
- Pin dependency versions.
- Preserve logs and validation results.
- Record enabled modalities and sampling limits.
- Regenerate the Statistics Card whenever the data or Dataset Card changes.
- Avoid storing sensitive raw values in the Statistics Card.

---

## Privacy and Governance

Statistics Cards should contain aggregate summaries rather than raw records.

Before sharing a Statistics Card:

- inspect small subgroup counts;
- remove direct and indirect identifiers;
- assess whether rare categories create re-identification risks;
- follow the governance constraints defined in the Dataset Card; and
- apply suppression or aggregation rules where required.

A structurally valid Statistics Card is not necessarily safe to release.

---

## Known Limitations

- Diagnostics depend on the accuracy of the SP1 variable roles and SP2 configuration.
- Mutual information and surrogate feature importance are exploratory rather than causal.
- PCA and correlation summaries may not capture nonlinear structure.
- Autocorrelation summaries do not constitute complete stationarity or seasonality testing.
- Entropy differences do not independently prove image artifacts or batch effects.
- Basic token counts cannot fully characterize semantic structure or text quality.
- Graph diagnostics currently provide structural summaries rather than complete community or topology analysis.
- The schema permits modality-specific extensions, so downstream consumers must handle optional fields.
- Large datasets may require additional sampling, distributed processing, or memory controls.

---

## Version History

| Version | Description |
|---|---|
| 1.0 | Initial release of the SP2 configuration, Statistics Card schema, modality-specific diagnostics, EDA prompt templates, examples, and build workflow |

---

## License

Use and redistribution are governed by the license provided at the repository root.
