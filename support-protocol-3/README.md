# SUPPORT PROTOCOL 3 – LLM Configuration Using Structured Form Responses

This directory contains the **non-paper assets** for **Support Protocol 3: LLM Configuration Using Structured Form Responses** in the DRAFT‑LLM workflow.

## 🎯 Purpose

SP3 acts as the "Policy Engine" of the DRAFT-LLM framework. It integrates the clinical intent from **SP1 (Dataset Card)** and the empirical evidence from **SP2 (Statistics Card)** to produce a machine-readable **LLM Configuration** (`llm_config.json`).

This configuration governs the "Intellectual Sparring Partner" behavior by defining:
- **Personas & Interaction:** Technical depth, explanation style, and auditor persona.
- **Governance & Safety:** Explicit boundaries on what the LLM can recommend, prohibited operations (e.g., using certain sensitive proxies), and required fairness metrics.
- **Data-Driven Guardrails:** Automated "risk flags" triggered by SP2 (e.g., if class imbalance > 20%, the LLM is forced to prioritize PR-curves over Accuracy).
- **Resource Constraints:** Compute budgets, allowed Python libraries, and environment limits.

---

## 📂 Contents

### ⚙️ Orchestration & Schema
- **`schema/llm_config.schema.json`**  
  Enforces the structure of the final config, including sections for `study_profile`, `governance`, `data_risk_flags`, and `base_system_prompt`.
- **`scripts/build_llm_config.py`**  
  The main driver. It maps cards to configurations and derives behavior flags from data distributions.
- **`scripts/consistency_checks.py`**  
  **The Feedback Loop:** Compares SP1 (Intent) vs. SP2 (Reality). For example, it flags an error if SP1 defines an "Equity Audit" but SP2 shows zero variance in the "Sensitive Attribute" column.

### 📝 Prompt Engineering
- **`prompts/system_prompt_template.md`**  
  The master template for the AI Auditor's persona. It includes placeholders for governance rules and study goals.
- **`prompts/user_prompt_templates.md`**  
  Modular templates for specific tasks: "EDA Feedback," "Model Selection Critiques," and "Stability Interpretation."
- **`scripts/prompt_builder.py`**  
  Compiles the templates and cards into concrete, ready-to-use prompt strings.

### 📄 Examples & Utils
- **`examples/llm_config_example.json`**  
  A reference output showing how a biological study's constraints are encoded.
- **`scripts/utils_io.py`**  
  Shared utilities for JSON/YAML handling and CLI logging.

---

## 🛠️ Dependencies

Requires a **Python 3.9+** environment with:
```bash
pip install pyyaml jsonschema pandas
```

---

## 🚀 Quickstart

### 1. Prepare Input Cards
Ensure you have a validated `dataset_card.json` (from SP1) and `statistics_card.json` (from SP2).

### 2. Generate the LLM Configuration
Run the builder to synthesize the cards into a policy:

```bash
python scripts/build_llm_config.py \
    --dataset-card ../support-protocol-1/my_dataset_card.json \
    --statistics-card ../support-protocol-2/my_statistics_card.json \
    --output examples/my_llm_config.json
```

### 3. Review Consistency Warnings
If `consistency_checks.py` detects a mismatch between your scientific goals (SP1) and your data (SP2), the script will output warnings or blocking errors. **Do not proceed to SP4 until these are resolved.**

---

## 🔗 Connection to Workflow
The **`llm_config.json`** is the final input for **Support Protocol 4 (Bundle Generation)**. SP4 will use this config to create the executable "Specialized Instructions" that drive the Basic Protocols (Generalization, Equity, Stability).
