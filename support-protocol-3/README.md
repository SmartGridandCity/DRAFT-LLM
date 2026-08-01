Step detected: **revise**

# Support Protocol 3 — LLM Configuration Using Structured Forms

**Version:** 1.0  
**Status:** Reference implementation

Support Protocol 3 (SP3) combines the study specification from **Support Protocol 1** with the empirical dataset summaries from **Support Protocol 2** to produce a validated, machine-readable **LLM Configuration**.

The resulting `llm_config.json` defines study-specific interaction preferences, governance requirements, resource limits, data-risk flags, and prompt templates for downstream DRAFT-LLM protocols.

---

## Purpose

SP3 serves as the configuration and policy layer of the DRAFT-LLM workflow.

It supports researchers in:

1. translating study goals into an explicit LLM study profile;
2. configuring interaction and code-generation preferences;
3. encoding governance, privacy, and interpretability requirements;
4. restricting recommended tools and methods according to available resources;
5. deriving risk flags from the SP2 Statistics Card;
6. checking consistency between the SP1 Dataset Card and SP2 Statistics Card;
7. generating study-specific system and user prompts; and
8. producing a validated LLM Configuration for Support Protocol 4.

SP3 configures LLM behavior but does not train, fine-tune, or evaluate a language model.

---

## Directory Structure

```text
support-protocol-3/
├── config/
│   └── sp3_config_example.yaml
├── examples/
│   ├── dataset_card_example.json
│   ├── llm_config_example.json
│   └── statistics_card_example.json
├── prompts/
│   ├── system_prompt_template.md
│   └── user_prompt_templates.md
├── schema/
│   └── llm_config.schema.json
├── scripts/
│   ├── build_llm_config.py
│   ├── consistency_checks.py
│   ├── prompt_builder.py
│   └── utils_io.py
└── README.md
```

---

## Files

### Configuration

#### `config/sp3_config_example.yaml`

Example configuration controlling how the final LLM Configuration is derived.

It defines:

- fallback project metadata;
- compute-budget classification;
- allowed libraries;
- environment restrictions;
- default user interaction preferences;
- privacy and interpretability defaults; and
- thresholds used to derive data-risk flags.

This file configures the SP3 generation process. It is not the final LLM Configuration.

Example:

```yaml
project_defaults:
  default_project_id: "example_study"
  default_intended_use: "internal_research"

resources:
  compute_budget: "medium"
  environment_constraints:
    - "offline_only"
  allowed_libraries:
    - "pandas"
    - "numpy"
    - "scikit-learn"

interaction_defaults:
  expertise: "intermediate"
  language: "python"
  interaction_style: "standard_explanations"
  code_style: "focused_examples"

governance_defaults:
  privacy_rules:
    - "no_raw_values_in_outputs"
  interpretability_requirements:
    - "justify_method_choice"

risk_thresholds:
  imbalance_ratio_high: 0.8
  missingness_rate_high: 0.2
```

Copy and customize this file rather than modifying the reference configuration directly.

---

### Schema

#### `schema/llm_config.schema.json`

Canonical JSON Schema for validating the generated LLM Configuration.

The schema defines the required structure for:

- project and source-card references;
- study and user profiles;
- governance constraints;
- resource constraints;
- data-risk flags;
- the instantiated system prompt; and
- reusable user prompt templates.

The version 1.0 schema uses JSON Schema Draft 7.

---

### Orchestration

#### `scripts/build_llm_config.py`

Main SP3 orchestration script. It:

1. loads the SP1 Dataset Card;
2. loads the SP2 Statistics Card;
3. loads the SP3 configuration;
4. performs cross-card consistency checks;
5. derives data-risk flags;
6. constructs study, user, governance, and resource profiles;
7. generates the system and user prompts;
8. validates the result against the schema; and
9. writes the final `llm_config.json`.

Blocking consistency errors stop generation unless the implementation’s explicit override option is used.

Overrides should be documented and should not replace scientific review.

---

### Consistency checks

#### `scripts/consistency_checks.py`

Compares the Dataset Card with the Statistics Card and returns:

- **warnings**, representing non-blocking issues requiring review; and
- **errors**, representing inconsistencies that should normally be resolved before continuing.

Checks may identify mismatches involving:

- outcomes;
- sensitive attributes;
- expected variables;
- sample structure;
- subgroup availability; and
- differences between declared study design and observed data.

The module reports inconsistencies but does not automatically repair the source cards.

---

### Prompt generation

#### `scripts/prompt_builder.py`

Builds:

- a concrete, study-specific base system prompt; and
- reusable prompts for EDA, modeling, and robustness tasks.

Prompt content is parameterized using the generated configuration, including:

- study goals;
- intended use;
- user expertise;
- programming language;
- governance rules;
- resource limits; and
- data-risk flags.

#### `prompts/system_prompt_template.md`

Human-readable template describing the intended structure of the generated system prompt.

#### `prompts/user_prompt_templates.md`

Reference templates for:

- exploratory data analysis;
- model and preprocessing recommendations; and
- robustness, generalization, equity, and stability checks.

The Python prompt builder is the executable source used by the current implementation. The Markdown templates should remain synchronized with it.

---

### Examples

#### `examples/dataset_card_example.json`

Example SP1 Dataset Card used as an input to SP3.

#### `examples/statistics_card_example.json`

Example SP2 Statistics Card containing outcome proportions, missingness summaries, and heterogeneity indicators.

#### `examples/llm_config_example.json`

Reference SP3 output illustrating the complete LLM Configuration structure.

---

### Utilities

#### `scripts/utils_io.py`

Shared utilities for:

- loading JSON files;
- loading YAML files;
- writing JSON outputs; and
- reporting file and parsing errors.

---

## Requirements

- Python 3.9 or later
- `PyYAML`
- `jsonschema`

Install the required dependencies:

```bash
python -m pip install \
  pyyaml \
  jsonschema
```

The SP3 scripts shown here do not require `pandas` unless additional consistency checks or data-processing extensions use it.

For reproducible execution, pin exact dependency versions in the repository environment or lockfile.

---

## Quick Start

### 1. Prepare the input cards

SP3 requires:

- a validated SP1 Dataset Card; and
- a validated SP2 Statistics Card.

Example inputs are available under:

```text
examples/dataset_card_example.json
examples/statistics_card_example.json
```

### 2. Create an SP3 configuration

Copy the example:

```bash
cp config/sp3_config_example.yaml config/my_sp3_config.yaml
```

Review and update:

- project defaults;
- compute budget;
- allowed libraries;
- environment constraints;
- interaction defaults;
- governance defaults; and
- risk thresholds.

### 3. Generate the LLM Configuration

Run the builder from the `support-protocol-3` directory:

```bash
python scripts/build_llm_config.py \
  --dataset-card examples/dataset_card_example.json \
  --statistics-card examples/statistics_card_example.json \
  --protocol-config config/my_sp3_config.yaml \
  --output-config examples/my_llm_config.json
```

Confirm the exact command-line arguments supported by the local implementation:

```bash
python scripts/build_llm_config.py --help
```

### 4. Review warnings and errors

The builder prints consistency findings to standard error.

```text
[WARN] ...
[ERROR] ...
```

Warnings should be reviewed before proceeding. Blocking errors should be resolved by correcting the Dataset Card, Statistics Card, or SP3 configuration.

If an override is necessary, document:

- the error;
- the reason for overriding it;
- the responsible reviewer;
- the expected effect; and
- the date of the decision.

### 5. Validate the output

The builder performs schema validation when `jsonschema` and the schema file are available.

The output can also be validated manually:

```bash
python -m jsonschema \
  -i examples/my_llm_config.json \
  schema/llm_config.schema.json
```

---

## Data-Risk Flags

SP3 derives behavioral cues from the Statistics Card using thresholds in the SP3 configuration.

Version 1.0 supports the following core flags:

| Flag | Meaning |
|---|---|
| `imbalance_flag` | At least one outcome meets or exceeds the configured class-proportion threshold |
| `must_discuss_imbalance` | Generated recommendations must address outcome imbalance |
| `missingness_flag` | At least one feature meets or exceeds the configured missingness threshold |
| `must_address_missingness` | Generated recommendations must address missing data |
| `heterogeneity_flag` | The Statistics Card reports strong subgroup structure |
| `emphasize_heterogeneity` | Generated recommendations must emphasize heterogeneity |

### Outcome imbalance

Given class proportions \(p_1, \ldots, p_k\), SP3 raises the imbalance flag when:

\[
\max_{j \in \{1,\ldots,k\}} p_j \geq \tau_{\mathrm{imbalance}}
\]

where \(\tau_{\mathrm{imbalance}}\) is configured by `imbalance_ratio_high`.

With the default threshold:

```yaml
imbalance_ratio_high: 0.8
```

a largest-class proportion of `0.80` or greater triggers the flag.

### Missingness

For feature missingness rates \(m_1, \ldots, m_d\), SP3 raises the missingness flag when:

\[
\max_{j \in \{1,\ldots,d\}} m_j \geq \tau_{\mathrm{missingness}}
\]

where \(\tau_{\mathrm{missingness}}\) is configured by `missingness_rate_high`.

### Heterogeneity

The current implementation reads a Statistics Card indicator such as:

```json
{
  "heterogeneity": {
    "has_strong_subgroups": true
  }
}
```

These flags are decision cues rather than definitive scientific conclusions. Their validity depends on the quality of the Statistics Card and the appropriateness of the configured thresholds.

---

## LLM Configuration Organization

The generated configuration generally contains:

| Section | Purpose |
|---|---|
| `project_id` | Study or project identifier |
| Source-card versions | Version or hash references for the SP1 and SP2 inputs |
| `study_profile` | Goal, analysis type, intended use, and study notes |
| `user_profile` | Expertise, language, interaction style, and code style |
| `governance` | Sensitive attributes, allowed uses, privacy rules, and prohibited operations |
| `resources` | Compute budget, allowed libraries, and environment constraints |
| `data_risk_flags` | Data-derived behavioral requirements |
| `base_system_prompt` | Fully instantiated system prompt |
| `prompt_templates` | EDA, modeling, and robustness prompts |

The authoritative field definitions are provided by:

```text
schema/llm_config.schema.json
```

---

## Governance and Safety

The governance section may specify:

```json
{
  "sensitive_attributes": ["gender", "race"],
  "allowed_uses": ["fairness_evaluation_only"],
  "privacy_rules": ["no_raw_values_in_outputs"],
  "forbidden_operations": [
    "targeted_marketing_by_sensitive_group"
  ],
  "interpretability_requirements": [
    "justify_method_choice"
  ]
}
```

Generated prompts instruct the LLM to respect these constraints. Prompt instructions alone, however, do not provide complete technical enforcement.

Production deployments should supplement prompts with:

- access controls;
- input and output validation;
- approved-tool allowlists;
- execution sandboxing;
- audit logging;
- human review; and
- organizational governance procedures.

---

## Reviewing the Generated Configuration

Before passing the configuration to SP4, review the following sections.

### Study profile

Confirm that:

- the goal matches the intended prediction or analysis task;
- the analysis type is appropriate;
- the intended use is accurately described; and
- high-stakes uses are explicitly identified.

### User profile

Confirm that:

- the expertise level is appropriate;
- the programming language is supported;
- the explanation style meets user needs; and
- the requested code style does not omit necessary safeguards.

### Governance

Confirm that:

- all sensitive attributes are represented;
- allowed uses are explicit;
- forbidden operations are complete;
- privacy requirements match the Dataset Card; and
- interpretability requirements are actionable.

### Resources

Confirm that:

- the compute budget is realistic;
- proposed libraries are permitted and available;
- offline or external-API restrictions are correct; and
- environment constraints are reflected in generated prompts.

### Data-risk flags

Compare the flags with the SP2 Statistics Card. In particular, verify:

- outcome class proportions;
- feature missingness rates;
- subgroup and batch heterogeneity; and
- whether the configured thresholds are scientifically appropriate.

### Generated prompts

Compare:

```text
base_system_prompt
prompt_templates
```

with:

```text
prompts/system_prompt_template.md
prompts/user_prompt_templates.md
```

Ensure that interpolated study, user, governance, resource, and risk information is accurate.

---

## Workflow Integration

The generated LLM Configuration is passed to Support Protocol 4.

```text
SP1 Dataset Card
        +
SP2 Statistics Card
        +
SP3 configuration defaults
        ↓
Consistency checks
        ↓
Profiles, constraints, and risk flags
        ↓
System and user prompt generation
        ↓
Validated LLM Configuration
        ↓
SP4 instruction bundle
        ↓
Generalization, equity, and stability audits
```

Whenever the Dataset Card, Statistics Card, governance rules, or risk thresholds change, regenerate the LLM Configuration and downstream instruction bundle.

---

## Reproducibility Recommendations

- Preserve the exact SP1 and SP2 inputs.
- Record input-card identifiers, versions, or hashes.
- Version the SP3 YAML configuration.
- Record the schema version.
- Pin dependency versions.
- Preserve warnings, errors, and validation results.
- Record any use of the override option.
- Store the generated prompts with the configuration.
- Review configuration changes through version control.
- Regenerate SP4 artifacts after every material SP3 change.

---

## Privacy Considerations

The LLM Configuration should contain policies and aggregate cues rather than raw observations.

Before sharing it:

- inspect study notes and prompts for sensitive information;
- avoid embedding raw patient or participant values;
- remove direct and indirect identifiers;
- review rare subgroup descriptions;
- verify that sensitive attributes appear only where authorized; and
- confirm compliance with the SP1 governance specification.

A schema-valid configuration is not necessarily safe or appropriate to release.

---

## Known Limitations

- Risk flags depend on the completeness and correctness of the Statistics Card.
- Fixed thresholds may not be appropriate for every outcome or domain.
- A class-proportion threshold does not capture every form of imbalance.
- Maximum feature missingness does not characterize missingness mechanisms.
- A binary heterogeneity indicator may oversimplify complex structure.
- Prompt-based governance does not guarantee policy compliance.
- Consistency checks cannot establish scientific, clinical, legal, or ethical validity.
- The generated prompts require qualified human review.
- Version 1.0 does not train or fine-tune the configured LLM.
- Version 1.0 does not automatically select specific metrics solely from risk flags.

---

## Version History

| Version | Description |
|---|---|
| 1.0 | Initial release of the SP3 configuration, schema, consistency checks, risk-flag derivation, prompt builder, examples, and LLM Configuration workflow |

---

## License

Use and redistribution are governed by the license provided at the repository root.
