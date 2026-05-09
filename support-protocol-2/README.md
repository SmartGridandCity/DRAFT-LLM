# SUPPORT PROTOCOL 2 – Dataset Structure and Advanced Summary Statistics for LLM Context

This directory contains the **non-paper assets** for **Support Protocol 2: Dataset Structure and Advanced Summary Statistics for LLM Context** in the DRAFT‑LLM workflow.

The goal of SP2 is to transform raw, high-dimensional biological data into a machine-readable **Statistics Card** (`statistics_card.json`). While SP1 captures what the researcher *intends* to do, SP2 captures what the data *actually allows*. DRAFT-LLM uses this empirical context to:
- **Ground the Audit:** Prevent the LLM from suggesting analyses that the data cannot support (e.g., auditing a subgroup with $N=0$).
- **Contextualize Performance:** Provide the "denominator" for metrics (e.g., prevalence for Brier scores).
- **Flag Technical Risks:** Automatically detect batch effects, entropy shifts, or extreme imbalance before modeling begins.

---

## 📂 Contents

### ⚙️ Orchestration & Schema
- **`config/sp2_config_example.yaml`**  
  Configuration file mapping data paths to specific modalities and preprocessing requirements.
- **`schema/statistics_card.schema.json`**  
  The JSON Schema used to validate the final output. This ensures the Statistics Card can be correctly parsed by the SP4 Instruction Bundle generator.
- **`scripts/build_statistics_card.py`**  
  The main orchestrator. It consumes an **SP1 Dataset Card** and the **SP2 Config**, executes the relevant modality scripts, and compiles the final `statistics_card.json`.

### 🧬 Modality-Specific Diagnostics (Modular)
- **`scripts/tabular_stats.py`**  
  Core diagnostics for clinical and omics tables: missingness, outcome imbalance, PCA/correlation summaries, and group-wise rates for sensitive attributes.
- **`scripts/timeseries_stats.py`**  
  Analysis of temporal coverage, stationarity, and outlier frequency in longitudinal data.
- **`scripts/image_stats.py`**  
  Computes resolution distributions and spectral entropy summaries (local/global) to detect tiling artifacts or staining variability.
- **`scripts/text_stats.py`**  
  Lexical richness and length distributions for clinical notes or pathology reports.
- **`scripts/graph_stats.py`**  
  Node/edge degree distributions and community indicators for biological networks or spatial graphs.

### 💡 LLM Integration
- **`prompts/eda_prompt_templates.md`**  
  Generic LLM prompt templates designed to consume the Statistics Card. These help the LLM perform "Automated EDA" and suggest modeling priorities based on data complexity.

---

## 🛠️ Dependencies

These scripts require a **Python 3.9+** environment. Install the core suite with:

```bash
pip install pandas numpy pyyaml scikit-learn pyarrow pillow scikit-image networkx statsmodels jsonschema
```

---

## 🚀 Quickstart

1. **Configure:** Edit `config/sp2_config_example.yaml` to point to your data files.
2. **Execute:** Run the orchestrator using your validated SP1 Card.
   ```bash
   python scripts/build_statistics_card.py \
     --dataset_card ../support-protocol-1/my_dataset_card.json \
     --config config/my_sp2_config.yaml \
     --output statistics_card.json
   ```
3. **Verify:** Check the output against the schema.
   ```bash
   # Automated within build_statistics_card.py, or manually:
   python -m jsonschema -i statistics_card.json schema/statistics_card.schema.json
   ```

---

## 🔗 Connection to Workflow
The output `statistics_card.json` is paired with the `dataset_card.json` from SP1. Together, they are ingested by **Support Protocol 3 (Configuration)** to set governance thresholds and **Support Protocol 4 (Bundle)** to generate the final audit instructions. 

For a worked example using genomic and clinical data, see `/examples/tcga_luad/sp2_stats_card.json`.