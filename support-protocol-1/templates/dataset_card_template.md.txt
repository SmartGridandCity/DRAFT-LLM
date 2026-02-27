# DRAFT-LLM Dataset Card

## 1. Card Metadata

- **Card ID:** {{card_id}}
- **Version:** {{version}}
- **Last updated:** {{last_updated}}
- **Prepared by:** {{prepared_by}}
- **Approved by:** {{approved_by}}
- **Data freeze date:** {{data_freeze_date}}
- **Notes:** {{notes}}

---

## 2. Study Overview

- **Title:** {{study_title}}
- **Primary question:** {{primary_question}}
- **Intended use (category):** {{intended_use}}
- **Intended use (details):** {{intended_use_details}}
- **Task types:** {{task_types}}
- **Secondary endpoints:** {{secondary_endpoints}}
- **Regulatory/decision context:** {{regulatory_context}}

---

## 3. Cohort Definition

- **Inclusion criteria:**
  - {{inclusion_criterion_1}}
  - {{inclusion_criterion_2}}
- **Exclusion criteria:**
  - {{exclusion_criterion_1}}
  - {{exclusion_criterion_2}}
- **Time origin:** {{time_origin}}
- **Approximate cohort size:** {{cohort_size_estimate}}

If multiple datasets:

- **Dataset roles:**
  - {{dataset_id}}: {{role}} (e.g., discovery, internal_validation, external_validation)

---

## 4. Data Sources

For each dataset:

### 4.1 Dataset {{dataset_id}}

- **Description:** {{dataset_description}}
- **Longitudinal:** {{is_longitudinal}}

Tables:

| Table ID | Table name        | Approx. rows | Approx. columns | Linkage keys         | Processing level | Time role      |
|---------|--------------------|-------------:|----------------:|----------------------|------------------|----------------|
| tbl1    | clinical_baseline  | 500          | 40              | patient_id           | normalized       | baseline       |
| tbl2    | gene_expression    | 500          | 20000           | patient_id, sample_id| normalized       | baseline       |
| ...     |                    |              |                 |                      |                  |                |

---

## 5. Variable Schema

For each variable across tables, record:

| Dataset ID | Table ID | Variable name | Description              | Canonical role        | Dtype       | Allowed values (if categorical) | Derived? | Use as predictor? | Leakage risk |
|-----------|----------|---------------|-------------------------|-----------------------|------------|-------------------------------|---------|-------------------|-------------|
| DS1       | clinical | age           | Age at diagnosis (years)| feature               | numeric    |                               | no      | yes               | none        |
| DS1       | clinical | sex           | Recorded legal sex      | sensitive_attribute   | categorical| male; female; other           | no      | maybe             | possible    |
| DS1       | outcome  | os_3yr_event  | 3-year OS event flag   | outcome               | binary     | 0; 1                          | yes     | no                | high        |
| ...       |          |               |                         |                       |            |                               |         |                   |             |

> The full variable dictionary can live in a separate spreadsheet; here, summarize the key variables and their roles.

---

## 6. Outcomes and Label Regimes

For each outcome:

### Outcome: {{outcome_name}}

- **Description:** {{outcome_description}}
- **Task type:** {{task_type}}
- **Time horizon:** {{time_horizon}}
- **Event / non-event codes:** {{event_label}} / {{non_event_label}}
- **Time column (if survival):** {{time_column}}
- **Censoring column (if survival):** {{censoring_column}}
- **Label source:** {{label_source}}
- **Label quality summary:** {{label_quality_summary}}
- **Primary for DRAFT audits?** {{primary_for_draft}}

---

## 7. Sensitive Attributes and Fairness-Relevant Subgroups

| Variable name | Dataset ID | Table ID | Governance status (required/recommended/optional/prohibited) | Reporting constraints (e.g., min cell size) | Subgroups of interest                          |
|--------------|-----------|---------|----------------------------------------------------------------|---------------------------------------------|-----------------------------------------------|
| sex          | DS1       | clinical| required                                                       | n >= 10 per cell                            | female vs male                                |
| race         | DS1       | clinical| prohibited                                                     | not reported                                | N/A                                           |
| center       | DS1       | clinical| required                                                       | aggregate small centers                     | Center A vs Center B+C                        |
| ...          |           |         |                                                                |                                             |                                               |

---

## 8. Constraints, Analysis Priorities, Practical Considerations

- **Expected sample size:** {{expected_sample_size}}
- **Approximate feature dimensionality:** {{approx_feature_dimensionality}}
- **Compute environment:** {{compute_environment}}
- **Access limitations:** {{access_limitations}}

- **Analysis priorities:** {{analysis_priorities}}
- **Required metrics:** {{required_metrics}}
- **Forbidden operations:** {{forbidden_operations}}

---

## 9. Edge Cases and Adaptations

- **Longitudinal / time-varying data:** {{longitudinal_notes}}
- **Unstructured modalities (e.g., images, text):** {{unstructured_representation_notes}}
- **Evolving dataset / registry notes:** {{registry_notes}}
- **Privacy / governance notes:** {{privacy_notes}}
