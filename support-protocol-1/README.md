# Support Protocol 1 — Study Intake and Dataset Card Construction

**Version:** 1.0  
**Status:** Reference implementation

Support Protocol 1 (SP1) converts study requirements, dataset characteristics, outcome definitions, and governance constraints into a validated, machine-readable **Dataset Card**.

The Dataset Card provides the study specification used by subsequent DRAFT-LLM protocols.

---

## Purpose

SP1 supports researchers in:

1. documenting the study objective and intended use;
2. defining cohorts, datasets, tables, and variables;
3. specifying outcomes and label regimes;
4. identifying sensitive attributes and fairness-relevant subgroups;
5. recording governance, resource, and analysis constraints; and
6. producing a Dataset Card that conforms to the canonical JSON Schema.

SP1 documents study design and intended data use. It does not perform statistical analysis or model training.

---

## Directory Structure

```text
support-protocol-1/
├── examples/
│   └── dataset_card_simple.json
├── schema/
│   └── dataset_card.schema.json
├── scripts/
│   ├── generate_dataset_card_from_intake.py
│   └── validate_dataset_card.py
├── templates/
│   ├── dataset_card_template.md
│   └── intake_form_template.csv
└── README.md
```

---

## Files

### `schema/dataset_card.schema.json`

Canonical JSON Schema for validating Dataset Cards.

### `templates/intake_form_template.csv`

Spreadsheet-oriented intake form for collecting study information from researchers and domain experts.

### `templates/dataset_card_template.md`

Human-readable template corresponding to the principal sections of the Dataset Card. It supports study planning, documentation, and review but does not replace the machine-readable JSON card.

### `examples/dataset_card_simple.json`

Minimal example of a completed Dataset Card.

### `scripts/generate_dataset_card_from_intake.py`

Converts a completed intake form into a preliminary JSON Dataset Card. The generated card may require manual completion before validation.

### `scripts/validate_dataset_card.py`

Validates a Dataset Card against the canonical schema and reports errors by JSON path.

---

## Requirements

- Python 3.10 or later
- `jsonschema`

Install the validation dependency:

```bash
python -m pip install "jsonschema>=4.18,<5"
```

Run the following commands from the `support-protocol-1` directory.

---

## Quick Start

### 1. Copy the intake form

```bash
cp templates/intake_form_template.csv my_study_intake.csv
```

Complete the copied form using a spreadsheet or text editor.

Document, where applicable:

- card identifier and version;
- study title and scientific question;
- intended use and task type;
- cohort definition;
- data sources and dataset roles;
- variables and canonical roles;
- outcomes and label regimes;
- sensitive attributes and fairness subgroups;
- governance requirements; and
- computational constraints and analysis priorities.

### 2. Generate a preliminary Dataset Card

```bash
python scripts/generate_dataset_card_from_intake.py \
  --input my_study_intake.csv \
  --output my_dataset_card.json
```

Review the generated card and complete any missing required fields.

> The generator creates a preliminary structure. Empty values, placeholders, or incomplete arrays may cause validation errors.

### 3. Validate the Dataset Card

```bash
python scripts/validate_dataset_card.py \
  --card my_dataset_card.json \
  --schema schema/dataset_card.schema.json
```

Successful validation returns exit status `0` and output similar to:

```text
OK: my_dataset_card.json is valid against schema/dataset_card.schema.json.
```

Failed validation returns exit status `1` and reports each error with its JSON path.

### 4. Validate the example card

```bash
python scripts/validate_dataset_card.py \
  --card examples/dataset_card_simple.json \
  --schema schema/dataset_card.schema.json
```

---

## Dataset Card Organization

| Section | Purpose |
|---|---|
| `card_metadata` | Card identifier, version, authorship, and data-freeze information |
| `study_overview` | Scientific question, intended use, and task type |
| `cohort` | Inclusion criteria, exclusion criteria, time origin, and dataset roles |
| `data_sources` | Datasets, tables, linkage keys, and processing information |
| `variables` | Variable definitions, data types, roles, and leakage risks |
| `outcomes` | Outcome definitions, coding, time horizons, and label provenance |
| `sensitive_attributes` | Sensitive variables and related governance restrictions |
| `fairness_subgroups` | Subgroups requiring equity assessment |
| `user_profile` | Intended user expertise and communication preferences |
| `governance_and_risk` | Data-use, privacy, and risk constraints |
| `constraints_and_priorities` | Resources, required metrics, and prohibited operations |

Implementations must use the field names defined by `dataset_card.schema.json`. Variable roles should use the schema-defined `canonical_role` field.

---

## Workflow Integration

A validated Dataset Card is passed to the downstream support protocols:

- **Support Protocol 2:** computes dataset statistics and structural summaries;
- **Support Protocol 3:** configures the language model, governance rules, and resource limits;
- **Support Protocol 4:** generates study-specific instructions, prompts, and code templates.

```text
Study intake
    ↓
SP1 Dataset Card
    ↓
Schema validation
    ↓
SP2 statistics + SP3 configuration
    ↓
SP4 instruction bundle
    ↓
Generalization, equity, and stability audits
```

Schema validation confirms structural conformity. It does not establish that the entered information is scientifically, clinically, or ethically correct.

---

## Reproducibility Recommendations

- Assign each Dataset Card a stable identifier.
- Use semantic versions such as `1.0.0`.
- Record update and data-freeze dates.
- Preserve the intake form used to generate the card.
- Validate the card after every modification.
- Regenerate downstream artifacts whenever the card changes.
- Store the card, schema version, and generated outputs together.
- Record significant changes in version control.

---

## Known Limitations

- The intake-to-JSON generator may produce a skeleton rather than a complete Dataset Card.
- Free-text responses may require manual conversion into structured fields.
- Schema validation cannot verify scientific or clinical accuracy.
- The Markdown template is intended for documentation and does not replace validated JSON.
- This directory provides a reference implementation and should be tested and adapted before production or regulated use.

---

## Version History

| Version | Description |
|---|---|
| 1.0 | Initial release of the SP1 intake, Dataset Card schema, templates, example, generation utility, and validation workflow |

---

## License

Use and redistribution are governed by the license provided at the repository root.