Step detected: **revise**

# Support Protocol 4 — Generation of Personalized Instructions for DRAFT Audits

**Version:** 1.0  
**Status:** Reference implementation

Support Protocol 4 (SP4) is the final assembly stage of the DRAFT-LLM support layer. It combines the validated outputs of Support Protocols 1–3 with reusable audit templates to generate a study-specific **Audit Instruction Bundle**.

The resulting `instruction_bundle.json` provides the system prompts, user prompt templates, and audit profiles used to instantiate the three Basic Protocols:

1. generalization;
2. equity; and
3. stability.

---

## Purpose

SP4 translates structured study metadata, empirical dataset summaries, governance constraints, and user priorities into reproducible audit instructions.

It supports researchers in:

1. extracting audit-relevant information from the SP1 Dataset Card;
2. incorporating empirical risks from the SP2 Statistics Card;
3. enforcing the governance and resource constraints defined by SP3;
4. enabling or disabling audits according to user priorities;
5. constructing audit-specific profiles;
6. rendering study-specific system and user prompts;
7. applying governance filters;
8. validating the completed instruction bundle; and
9. recording source versions and generation metadata.

SP4 generates instructions and prompts. It does not execute statistical analyses, train predictive models, or replace scientific review.

---

## Directory Structure

```text
support-protocol-4/
├── configs/
│   ├── audit_templates.json
│   └── user_focus.example.json
├── examples/
│   └── instruction_bundle_example.json
├── schema/
│   └── audit_instruction_bundle.schema.json
├── scripts/
│   └── build_instruction_bundle.py
├── sp4/
│   ├── __init__.py
│   ├── extractor.py
│   ├── profiles.py
│   ├── prompts.py
│   └── validate.py
└── README.md
```

The exact contents may vary by repository release. The schema and executable modules are the authoritative implementation sources.

---

## Inputs

SP4 requires three validated artifacts and one audit-template configuration.

### SP1 Dataset Card

The Dataset Card provides:

- study objectives;
- intended use;
- outcome definitions;
- variable roles;
- sensitive attributes;
- grouping and time variables;
- governance requirements; and
- study-level constraints.

### SP2 Statistics Card

The Statistics Card provides:

- sample and feature counts;
- outcome distributions;
- missingness summaries;
- subgroup sizes;
- dependence indicators;
- heterogeneity indicators;
- temporal or site structure; and
- other modality-specific diagnostics.

### SP3 LLM Configuration

The LLM Configuration provides:

- the study profile;
- the user interaction profile;
- governance constraints;
- prohibited operations;
- resource limits;
- allowed libraries;
- data-driven risk flags; and
- base prompt requirements.

### Audit templates

The audit-template file provides method-agnostic blueprints for:

- generalization;
- equity; and
- stability.

These templates define audit objectives, system-prompt structures, and reusable user-prompt tasks.

---

## Files

### Schema

#### `schema/audit_instruction_bundle.schema.json`

Canonical JSON Schema for validating the generated Audit Instruction Bundle.

The bundle contains:

- a project identifier;
- source-protocol versions;
- a generation timestamp; and
- an `audits` object containing enabled audit instructions.

Each audit must include:

```json
{
  "system_prompt": "Study-specific audit instructions",
  "user_prompt_templates": {
    "plan": "Task-specific prompt"
  },
  "profile": {
    "audit-specific parameters": "..."
  }
}
```

The version 1.0 schema uses JSON Schema Draft 7.

---

### Audit templates

#### `configs/audit_templates.json`

Defines reusable templates for each Basic Protocol.

Each audit template contains:

- an audit objective;
- a system-prompt template; and
- one or more user-prompt templates.

Template placeholders use double braces:

```text
{{study_profile.goal}}
{{outcome_variable}}
{{governance.sensitive_attributes}}
{{resources.compute_budget}}
```

SP4 replaces these placeholders with values extracted from the input cards and LLM Configuration.

Templates should remain method-agnostic. Dataset-specific values belong in the input artifacts or generated bundle rather than in this file.

---

### User focus

#### `configs/user_focus.example.json`

Optional configuration controlling which audits are generated and how they are prioritized.

Example:

```json
{
  "enabled_audits": [
    "generalization",
    "equity",
    "stability"
  ],
  "priority_order": [
    "generalization",
    "equity",
    "stability"
  ],
  "priority_subgroups": [
    "race",
    "gender"
  ],
  "notes": "Run generalization first, followed by equity and stability."
}
```

Supported audit names are:

```text
generalization
equity
stability
```

If `enabled_audits` is absent or empty, all three audits are generated.

The current builder uses `enabled_audits` directly. Other fields, including `priority_order`, `priority_subgroups`, and `notes`, affect output only if the profile or extraction modules explicitly process them.

---

### Orchestration

#### `scripts/build_instruction_bundle.py`

Main SP4 orchestration script. It:

1. loads the Dataset Card;
2. loads the Statistics Card;
3. loads the LLM Configuration;
4. loads the audit templates;
5. loads the optional user-focus configuration;
6. identifies enabled audits;
7. extracts audit and template context;
8. constructs audit-specific profiles;
9. generates system and user prompts;
10. applies governance filters;
11. adds metadata and a generation timestamp;
12. validates the resulting bundle; and
13. writes the bundle as JSON.

---

### Logic modules

#### `sp4/extractor.py`

Extracts and normalizes audit-relevant context from the input artifacts.

Typical values include:

- study goal;
- intended use;
- outcome variable and task type;
- sensitive attributes;
- grouping keys;
- subgroup counts;
- sample structure;
- risk flags; and
- resource constraints.

It should distinguish between:

- values used to build audit profiles; and
- values used to interpolate prompt templates.

#### `sp4/profiles.py`

Constructs the profile associated with each enabled audit.

Profiles may contain:

- candidate evaluation designs;
- recommended metrics;
- grouping or temporal variables;
- subgroup priorities;
- risk warnings;
- resource constraints; and
- interpretation requirements.

Profiles are study-specific recommendations, not immutable statistical decisions. Their appropriateness must be reviewed by a qualified analyst.

#### `sp4/prompts.py`

Loads audit templates and interpolates study-specific context into:

- audit system prompts; and
- user prompt templates.

The module should report unresolved required placeholders rather than silently generating incomplete prompts.

#### `sp4/validate.py`

Provides final validation and governance utilities, including:

- governance filtering;
- source-version metadata;
- timestamp generation; and
- JSON Schema validation.

Governance filtering supplements but does not replace execution controls or human review.

---

## Requirements

- Python 3.9 or later
- `jsonschema`

Install the dependency:

```bash
python -m pip install jsonschema
```

For reproducible execution, use pinned dependency versions in a lockfile or environment specification.

---

## Quick Start

### 1. Prepare the inputs

Ensure that the following artifacts are available and valid:

```text
dataset_card.json
statistics_card.json
llm_config.json
configs/audit_templates.json
```

Optionally prepare:

```text
configs/user_focus.json
```

### 2. Review the audit templates

Before generation, confirm that:

- template placeholders match the extraction context;
- audit requirements are appropriate for the study;
- governance language is complete;
- resource limits are represented; and
- no dataset-specific values are hard-coded.

### 3. Generate the instruction bundle

Run the builder from the `support-protocol-4` directory:

```bash
python scripts/build_instruction_bundle.py \
  --dataset-card ../support-protocol-1/dataset_card.json \
  --statistics-card ../support-protocol-2/statistics_card.json \
  --llm-config ../support-protocol-3/llm_config.json \
  --audit-templates configs/audit_templates.json \
  --user-focus configs/user_focus.example.json \
  --project-id example_project \
  --out instruction_bundle.json
```

Confirm the supported arguments:

```bash
python scripts/build_instruction_bundle.py --help
```

### 4. Validate the output

The builder calls the bundle validator before writing the final output.

The bundle can also be validated manually:

```bash
python -m jsonschema \
  -i instruction_bundle.json \
  schema/audit_instruction_bundle.schema.json
```

Schema validation confirms structural conformity. It does not establish that the audit instructions are scientifically, ethically, or clinically appropriate.

---

## Audit Profiles

### Generalization

The generalization audit evaluates whether predictive performance is likely to extend beyond the training observations.

Its generated instructions may address:

- cross-validation design;
- grouped or temporal splitting;
- leakage prevention;
- external validation;
- outcome-appropriate performance metrics;
- calibration;
- class imbalance;
- dependence between observations; and
- distribution shift.

Example profile elements include:

```json
{
  "grouping_key": "site_id",
  "recommended_designs": [
    "grouped_cross_validation",
    "temporal_validation"
  ],
  "risk_flags": [
    "imbalance",
    "site_heterogeneity"
  ]
}
```

### Equity

The equity audit evaluates performance and calibration across permitted sensitive groups.

Its generated instructions may address:

- subgroup sample sizes;
- subgroup performance;
- subgroup calibration;
- uncertainty intervals;
- intersectional analyses;
- privacy-preserving reporting;
- minimum reporting thresholds; and
- governance restrictions.

Equity analysis must not be generated for unavailable, unauthorized, or unusably sparse sensitive attributes without an explicit warning.

### Stability

The stability audit evaluates whether model behavior, predictive features, or evidence patterns remain consistent across resamples and relevant perturbations.

Its generated instructions may address:

- feature-selection stability;
- performance variation across resamples;
- sensitivity to model choice;
- temporal or site perturbations;
- subgroup-specific stability;
- rank correlations;
- selection frequencies;
- Jaccard similarity; and
- uncertainty in scientific interpretation.

The feature granularity and number of tracked elements should be derived from SP2, constrained by SP3, and held fixed during comparisons. Otherwise, apparent instability may reflect changes in the extraction procedure rather than changes in model behavior.

---

## Template Interpolation

Audit templates contain placeholders such as:

```text
{{study_profile.goal}}
{{outcome_variable}}
{{summary_of_size_and_structure}}
{{data_risk_flags_summary}}
{{governance.sensitive_attributes}}
{{resources.compute_budget}}
```

SP4 should verify that:

1. every required placeholder has a source;
2. inserted values use the expected type;
3. lists are rendered consistently;
4. missing optional values receive an explicit neutral representation; and
5. unresolved placeholders are reported.

A generated prompt containing unresolved `{{...}}` fields should not be considered complete.

---

## Governance Filtering

Before validation, SP4 applies governance filters using the SP3 governance configuration.

These filters may:

- remove prohibited recommendations;
- restrict subgroup analyses;
- prevent disallowed model classes;
- enforce privacy language;
- restrict external services;
- require interpretability; and
- attach warnings to high-risk uses.

Prompt-level filtering is not a security boundary. Production deployments should also use:

- access controls;
- tool and library allowlists;
- execution sandboxing;
- input and output validation;
- privacy review;
- audit logging; and
- qualified human oversight.

---

## Output Structure

A generated bundle has the following general structure:

```json
{
  "project_id": "example_project",
  "sp1_version": "1.0",
  "sp2_version": "1.0",
  "sp3_version": "1.0",
  "generated_at": "2026-08-01T15:00:00Z",
  "audits": {
    "generalization": {
      "system_prompt": "...",
      "user_prompt_templates": {
        "plan": "...",
        "refine": "..."
      },
      "profile": {}
    },
    "equity": {
      "system_prompt": "...",
      "user_prompt_templates": {
        "plan": "...",
        "subgroup_analysis": "..."
      },
      "profile": {}
    },
    "stability": {
      "system_prompt": "...",
      "user_prompt_templates": {
        "plan": "...",
        "sensitivity_analysis": "..."
      },
      "profile": {}
    }
  }
}
```

The authoritative field definitions are provided by:

```text
schema/audit_instruction_bundle.schema.json
```

---

## Workflow Integration

```text
SP1 Dataset Card
        +
SP2 Statistics Card
        +
SP3 LLM Configuration
        +
Audit templates and optional user focus
        ↓
Context extraction
        ↓
Audit-profile construction
        ↓
Prompt interpolation
        ↓
Governance filtering
        ↓
Metadata and schema validation
        ↓
SP4 Audit Instruction Bundle
        ↓
Basic Protocol 1: Generalization
Basic Protocol 2: Equity
Basic Protocol 3: Stability
```

The bundle is conditional on the exact SP1–SP4 versions used. If study goals, data, statistics, governance constraints, templates, or user priorities change, regenerate the bundle and rerun the affected Basic Protocols.

---

## Reviewing the Generated Bundle

Before using the bundle, review the following.

### Source metadata

Confirm that:

- the project identifier is correct;
- source-protocol versions are accurate;
- the generation timestamp is present; and
- the bundle corresponds to the intended input files.

### Enabled audits

Confirm that:

- the required audits are present;
- disabled audits are absent;
- the audit order matches the intended workflow; and
- user priorities have been applied where supported.

### Audit profiles

Confirm that:

- proposed designs match the study structure;
- metrics match the outcome type;
- subgroup analyses are supported by the data;
- resource limits are realistic; and
- risk flags agree with the Statistics Card.

### Generated prompts

Confirm that:

- all placeholders were resolved;
- study goals and outcomes are correct;
- governance constraints are visible;
- prohibited operations are excluded;
- prompts do not contain sensitive raw data; and
- conclusions are appropriately calibrated.

---

## Reproducibility Recommendations

- Preserve the exact SP1, SP2, and SP3 input files.
- Record input identifiers, versions, and cryptographic hashes.
- Version the audit templates and user-focus configuration.
- Record the SP4 schema and software version.
- Preserve the generated timestamp.
- Pin dependency versions.
- Store validation results with the bundle.
- Record any manual modifications after generation.
- Regenerate the bundle after every material upstream change.
- Do not reuse earlier audit conclusions after changing the bundle.

---

## Privacy Considerations

The instruction bundle should contain structured context and aggregate summaries rather than raw participant-level information.

Before sharing it:

- remove direct and indirect identifiers;
- inspect interpolated prompts for raw values;
- review rare subgroup descriptions;
- suppress unsafe small-count information;
- confirm that sensitive attributes are used only as permitted;
- verify that governance restrictions remain intact; and
- assess whether profiles expose confidential study details.

A schema-valid instruction bundle is not necessarily safe to distribute.

---

## Known Limitations

- Generated instructions depend on the quality of all upstream artifacts.
- Template interpolation cannot determine whether a recommendation is scientifically valid.
- Fixed audit templates may not cover every modality or study design.
- User priorities are only effective when explicitly processed by the implementation.
- Small or missing subgroups may prevent meaningful equity analysis.
- Risk flags may simplify complex statistical conditions.
- Prompt-based governance does not guarantee compliant model behavior.
- Schema validation does not test semantic correctness.
- Audit profiles require qualified human review.
- SP4 does not execute the Basic Protocols.
- SP4 does not independently verify claims produced by an LLM.

---

## Version History

| Version | Description |
|---|---|
| 1.0 | Initial release of the SP4 schema, audit templates, user-focus configuration, context extraction, audit profiles, prompt generation, governance filtering, and instruction-bundle workflow |

---

## License

Use and redistribution are governed by the license provided at the repository root.
