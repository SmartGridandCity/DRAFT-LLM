Step detected: **scope / revise (SP1 Documentation)**

Here is the revised **Support Protocol 1 (SP1)** README. It has been polished to align with the root-level generic structure, ensuring it serves as the foundational "Intake" layer for the DRAFT-LLM workflow.

---

# SUPPORT PROTOCOL 1 – Study Intake and Dataset Card Construction

This directory contains the **non-paper assets** for **Support Protocol 1: Study Intake and Dataset Card Construction** in the DRAFT‑LLM workflow.

The objective of SP1 is to formalize and standardize study metadata, prediction tasks, and governance constraints into a machine-readable **Dataset Card**. This card serves as the "Source of Truth" for DRAFT‑LLM, allowing it to generate study-specific Specialized Instructions for downstream audits (**Generalization, Equity, and Stability**).

---

## 📂 Contents

- **`schema/dataset_card.schema.json`**  
  The canonical JSON Schema for dataset cards. This ensures that any card produced is valid and compatible with the DRAFT‑LLM generation engine (SP4).

- **`templates/intake_form_template.csv`**  
  A tabular intake form for researchers and domain experts. It captures clinical intent, variable roles (Target, Sensitive, Technical), and cohort criteria in a spreadsheet-friendly format.

- **`templates/dataset_card_template.md`**  
  A human-readable markdown template that mirrors the JSON schema. Ideal for documentation and peer review of study designs.

- **`examples/dataset_card_simple.json`**  
  A minimal example of a single-center, cross-sectional biological study.

- **`examples/dataset_card_multicenter_longitudinal.json`**  
  A complex example demonstrating how to represent multi-site data, temporal shifts, and longitudinal tracking.

- **`scripts/validate_dataset_card.py`**  
  A utility script to validate a `.json` dataset card against the schema. Use this before proceeding to Support Protocol 2.

- **`scripts/generate_dataset_card_from_intake.py`**  
  An automation script that maps a completed `intake_form_template.csv` to a structured `dataset_card.json` skeleton for manual refinement.

---

## 🚀 Quickstart

### 1. Fill the Intake Form
Domain experts should define the study parameters. Copy the template and fill it using any spreadsheet editor:

```bash
cp templates/intake_form_template.csv my_study_intake.csv
```

### 2. Generate the JSON Dataset Card
Convert the CSV intake into the standardized JSON format:

```bash
python scripts/generate_dataset_card_from_intake.py --input my_study_intake.csv --output my_dataset_card.json
```

### 3. Validate and Refine
Ensure the card meets the DRAFT-LLM requirements:

```bash
python scripts/validate_dataset_card.py --card my_dataset_card.json
```

---

## 🔗 Connection to Workflow
Once `my_dataset_card.json` is validated, it is passed to **Support Protocol 2 (Statistics)** to be enriched with empirical data summaries, eventually forming the context for the DRAFT-LLM audit instructions.
