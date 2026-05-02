# Support Protocol 4 – Generation of Personalized Instructions for DRAFT Audits

This module implements **Support Protocol 4: Generation of Personalized Instructions for DRAFT Audits**.

Support Protocol 4 uses:

- the **dataset card** (Support Protocol 0),
- the **statistics card** (Support Protocol 1),
- the **LLM configuration** (Support Protocol 2), and
- **method-agnostic DRAFT audit templates**

to generate a **personalized DRAFT‑LLM instruction bundle** for:

- Generalization audit (Basic Protocol 1),
- Equity audit (Basic Protocol 2),
- Stability / robustness audit (Basic Protocol 3, if applicable).

The output bundle provides:

- **Concrete system prompts** (one per audit type).
- **Concrete user prompt templates** (e.g., `plan`, `refine`, `subgroup_analysis`).
- **Structured audit profiles** that encode design choices for each audit.

The bundle is intended to be consumed by an orchestration layer that runs the
DRAFT Basic Protocols, ensuring that all LLM interactions are:

- study‑aware,
- data‑aware, and
- governance‑compliant.

---

## 1. Inputs

Support Protocol 4 expects:

1. **Dataset card (SP0)** – JSON  
   Includes:
   - Study goals and intended use.
   - Data description and key variables (including outcome and sensitive attributes).
   - User profile (expertise, language, explanation style).
   - Governance and risk constraints.
   - Resource constraints.

2. **Statistics card (SP1)** – JSON  
   Includes:
   - Global and subgroup statistics.
   - Outcome distributions, imbalance, missingness.
   - Indicators of dependence, heterogeneity, or other relevant structure.

3. **LLM configuration (SP2)** – JSON  
   Typically produced by Support Protocol 3. Includes:
   - `study_profile` (goal, analysis_type, intended_use, risk_level).
   - `user_profile` (expertise, interaction_style, code_style, language).
   - `governance` (sensitive_attributes, allowed_uses, forbidden_operations, interpretability_requirements).
   - `resources` (compute_budget, allowed_libraries, environment_constraints).
   - `data_risk_flags` (e.g., `imbalance_flag`, `must_discuss_imbalance`, `heterogeneity_flag`).
   - `base_system_prompt` (string).
   - `prompt_templates` (generic EDA/modeling/robustness templates).

4. **DRAFT audit templates** – JSON (`configs/audit_templates.json`)  
   Method‑agnostic “blueprints” for:
   - Generalization audit (Basic Protocol 1),
   - Equity audit (Basic Protocol 2),
   - Stability / robustness audit (Basic Protocol 3).
   These describe **what each audit should achieve** (e.g., cross‑validation,
   subgroup performance comparison, feature stability), not yet tailored to a
   particular study.

5. **(Optional) User‑selected audit focus** – JSON  
   - Which audits to prioritize (e.g., run `["generalization", "equity"]` first).
   - Optional priority areas (e.g., specific subgroups or features of concern).

---

## 2. High‑level workflow

Support Protocol 4 proceeds in four steps:

1. **Extract audit‑relevant parameters** from SP0–SP2 (`sp4.extractor`).
2. **Instantiate audit profiles** (generalization, equity, stability) tailored
   to the study (`sp4.profiles`).
3. **Generate audit‑specific system and user prompts** (`sp4.prompts`).
4. **Validate and package** them into a DRAFT‑LLM instruction bundle
   (`sp4.validate` and `scripts/build_instruction_bundle.py`).

The final instruction bundle conforms to:
`schema/audit_instruction_bundle.schema.json`.

---

## 3. Quickstart

### 3.1 Install

This module only uses Python standard library; a `requirements.txt` is provided
for convenience if you wish to add optional tooling.

```bash
cd support-protocol-4
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
