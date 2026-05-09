# SUPPORT PROTOCOL 4 – Generation of Personalized Instructions for DRAFT Audits

This directory contains the **non-paper assets** for **Support Protocol 4: Generation of Personalized Instructions for DRAFT Audits** in the DRAFT‑LLM workflow.

## 🎯 Purpose

Support Protocol 4 is the final "Assembly" stage of the support layer. It ingests the validated artifacts from the previous protocols to generate a **DRAFT‑LLM Instruction Bundle** (`instruction_bundle.json`). 

This bundle is a study-specific package that tells the LLM exactly how to behave during the three Basic Protocols (Generalization, Equity, and Stability). By "compiling" the instructions here, we ensure that the audits are:
- **Consistent:** Every audit run uses the same system prompts and decision logic.
- **Context-Aware:** The LLM knows the specific subgroups (from SP1/SP2) and governance rules (from SP3).
- **Audit-Ready:** It provides the LLM with the "Audit Profile"—the metrics, thresholds, and comparison strategies relevant to the specific biological task.

---

## 📂 Contents

### ⚙️ Orchestration & Schema
- **`schema/audit_instruction_bundle.schema.json`**  
  The JSON Schema for the final output. It defines the structure for `generalization_audit`, `equity_audit`, and `stability_audit` sections.
- **`scripts/build_instruction_bundle.py`**  
  The main compiler script. It pulls data from SP1, SP2, and SP3, applies them to the audit templates, and generates the final JSON package.
- **`configs/audit_templates.json`**  
  Method-agnostic "blueprints" for the three Basic Protocols. These define the *logic* of an audit (e.g., "Compare performance across sites") without being tied to a specific dataset.

### 🧩 Logic Modules
- **`sp4/extractor.py`:** Pulls audit-relevant parameters (e.g., list of sensitive attributes, outcome type) from the cards.
- **`sp4/profiles.py`:** Tailors the audit profiles (e.g., selecting "Brier Score" for probability-calibrated tasks).
- **`sp4/prompts.py`:** Injects the study-specific context into the audit system prompts.

---

## 📥 Inputs Required

1.  **Dataset Card (SP1):** For study goals and variable roles.
2.  **Statistics Card (SP2):** For empirical risk flags (imbalance, missingness).
3.  **LLM Configuration (SP3):** For governance rules, personas, and system-wide prompts.

---

## 🚀 Quickstart

### 1. Installation
This module primarily uses the Python standard library with `jsonschema` for validation.

```bash
pip install jsonschema
```

### 2. Generate the Instruction Bundle
Ensure your SP1, SP2, and SP3 JSON files are ready.

```bash
python scripts/build_instruction_bundle.py \
    --sp1 ../support-protocol-1/dataset_card.json \
    --sp2 ../support-protocol-2/statistics_card.json \
    --sp3 ../support-protocol-3/llm_config.json \
    --output instruction_bundle.json
```

---

## 🔗 Connection to Workflow
The **`instruction_bundle.json`** is the direct input for the three **Basic Protocols (BP)**:
- **BP1 (Generalization):** Uses the `generalization_audit` profile.
- **BP2 (Equity):** Uses the `equity_audit` profile + sensitive attributes.
- **BP3 (Stability):** Uses the `stability_audit` profile + technical covariates.

For a complete end-to-end example (TCGA Case Study), see `/examples/tcga_luad/sp4_instruction_bundle.json`.
