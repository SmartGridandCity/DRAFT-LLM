# SUPPORT PROTOCOL 1 – Study Intake and Dataset Card Construction

This repository contains the *non-paper assets* for **Support Protocol 1: Study Intake and Dataset Card Construction** in DRAFT‑LLM.

The goal is to standardize how study metadata and dataset structure are represented in a **dataset card** that DRAFT‑LLM can parse to generate a study‑specific Specialized Instruction for the DRAFT audits (generalization, equity, stability).

---

## Contents

- `schema/dataset_card.schema.json`  
  Canonical JSON Schema for dataset cards. Used to validate cards before they are consumed by DRAFT‑LLM.

- `templates/intake_form_template.csv`  
  Simple, tabular intake form template capturing the information needed to construct a dataset card (can be uploaded to REDCap/Qualtrics, or edited in a spreadsheet).

- `templates/dataset_card_template.md`  
  Human‑readable markdown template for a dataset card, mirroring the structure of the JSON representation.

- `examples/dataset_card_simple.json`  
  Minimal example dataset card for a single‑center, cross‑sectional study.

- `examples/dataset_card_multicenter_longitudinal.json`  
  Example dataset card illustrating multi‑center and longitudinal data.

- `scripts/validate_dataset_card.py`  
  Python script to validate a dataset card JSON file against the canonical schema.

- `scripts/generate_dataset_card_from_intake.py`  
  Example script that converts a completed intake form (CSV) into a skeleton dataset card JSON that can be manually refined.

---

## Quickstart

### 1. Fill the intake form

1. Copy `templates/intake_form_template.csv` to a new file, e.g.:

   ```bash
   cp templates/intake_form_template.csv my_study_intake.csv
