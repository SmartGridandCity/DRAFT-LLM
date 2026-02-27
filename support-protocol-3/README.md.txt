# Support Protocol 3 – LLM Configuration Using Structured Form Responses

## Purpose

Support Protocol 3 converts two structured artifacts:

- **Dataset card (Support Protocol 0)** – declarative description of:
  - Study goals and task framing
  - Data sources and structures
  - Key variables and their roles (outcome, predictors, sensitive attributes, technical covariates)
  - User profile and interaction preferences
  - Governance, risk, and resource constraints

- **Statistics card (Support Protocol 1)** – empirical summary of:
  - Global statistics and basic distributions
  - Class / outcome imbalance and missingness
  - Dependence / heterogeneity indicators
  - Other salient complexity or risk flags

into a **machine-readable LLM configuration** that governs how the LLM will assist in the study.

The configuration controls:

- System and user prompt templates
- Interaction style and level of technical depth
- Modeling and tool suggestions (EDA, robustness checks, fairness, stability)
- Safety, governance, and resource constraints
- Data-driven behavior flags (e.g., must discuss imbalance / missingness / heterogeneity)

Support Protocol 3 outputs:

1. A validated **LLM configuration JSON**.
2. A small set of **prompt templates** (system + user) that can be assembled into
   personalized instruction bundles by downstream workflows.

---

## Files and components

### `config/sp3_config_example.yaml`

A minimal example of high-level configuration options for this protocol itself
(e.g., default resource budgets, allowed libraries). This is **not** the final
LLM configuration; it guides how `build_llm_config.py` behaves.

### `schema/llm_config.schema.json`

JSON Schema for validating the LLM configuration object produced by this protocol.
It enforces required sections:

- `project_id`, `sp0_version`, `sp1_version`
- `study_profile`
- `user_profile`
- `governance`
- `resources`
- `data_risk_flags`
- `base_system_prompt`
- `prompt_templates`

### `scripts/utils_io.py`

Utility functions for robust I/O:

- Load and save JSON
- Load YAML
- Basic CLI-friendly error handling

### `scripts/consistency_checks.py`

Implements the **consistency checks and feedback loop (Support 0 ↔ Support 1)**:

- Cross-checks key elements between dataset and statistics cards:
  - Outcome variable
  - Sensitive attributes
  - Basic size and outcome-type compatibility
- Returns:
  - A list of non-fatal warnings
  - A list of blocking errors that should be resolved before proceeding

In an automated pipeline, blocking errors should trigger a revision of Support 0
or Support 1 before building the LLM configuration.

### `scripts/prompt_builder.py`

Builds:

- A **concrete base system prompt** string using the configuration.
- A small dictionary of **short user prompt templates** (EDA, modeling, robustness).

These follow the structure described in Support Protocol 3 and are intended to
be generic but parameterized by the configuration.

### `scripts/build_llm_config.py`

Main driver script for Support Protocol 3.

Responsibilities:

1. Load:
   - Dataset card (SP0)
   - Statistics card (SP1)
   - Optional protocol configuration (YAML)

2. Run consistency checks:
   - If blocking errors are found, prints them and exits (unless `--force` is used).

3. Map cards → LLM configuration:
   - Extract study goal, task framing, and intended use
   - Extract user profile and interaction style
   - Extract governance and resource constraints
   - Derive data risk flags (imbalance, missingness, heterogeneity, etc.) from the statistics card

4. Build prompts:
   - Instantiate a **base system prompt** from `prompts/system_prompt_template.md` and the config
   - Attach **user prompt templates** from `prompts/user_prompt_templates.md`

5. Validate against `schema/llm_config.schema.json`.

6. Save the final configuration to disk (JSON).

### `examples/`

- `dataset_card_example.json` – small, generic example dataset card (SP0).
- `statistics_card_example.json` – small, generic example statistics card (SP1).
- `llm_config_example.json` – example of the final LLM configuration authored
  to match the schema and the Support Protocol 3 description.

### `prompts/`

- `system_prompt_template.md` – template for the LLM system prompt with placeholders.
- `user_prompt_templates.md` – collection of short user prompt templates for EDA,
  modeling, and robustness.

---

## Quickstart

### 1. Prepare cards (SP0 and SP1)

Create JSON files for:

- `dataset_card.json` (Support Protocol 0)
- `statistics_card.json` (Support Protocol 1)

You can start from `examples/dataset_card_example.json` and
`examples/statistics_card_example.json`.

### 2. Build the LLM configuration

From the `support-protocol-3/` directory:

```bash
python -m scripts.build_llm_config \
    --dataset-card examples/dataset_card_example.json \
    --statistics-card examples/statistics_card_example.json \
    --output-config examples/llm_config_generated.json
