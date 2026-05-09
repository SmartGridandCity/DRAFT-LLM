\# DRAFT-LLM: Dataset Readiness Assessment for Training



Implementation of the DRAFT protocol for auditing high-dimensional biological data.



\## 📁 Repository Structure



\### 🛠️ Support Protocols (Generic - Root)

These folders contain the infrastructure to process any biological dataset.

\- `/support-protocol-1/`: \*\*Study Intake.\*\* Templates and schemas for defining goals and variable roles.

\- `/support-protocol-2/`: \*\*Statistics Card.\*\* Scripts to generate disaggregated data profiles.

\- `/support-protocol-3/`: \*\*LLM Config.\*\* Personas, governance rules, and prompt templates.

\- `/support-protocol-4/`: \*\*Bundle Generation.\*\* Logic to compile SP1-3 into specific audit instructions.



\### 🧪 Examples (Case Study)

\- `/examples/tcga\_luad/`: Complete DRAFT implementation for Lung Adenocarcinoma mortality prediction.

&#x20; - `sp1\_dataset\_card.json`: The specific intake for TCGA-LUAD.

&#x20; - `sp2\_stats\_card.json`: Empirical statistics for this cohort.

&#x20; - `sp3\_config.json`: Auditor constraints and safety settings.

&#x20; - `sp4\_instruction\_bundle.json`: The compiled instruction for the LLM.

&#x20; - `bp1\_generalization.ipynb`: \*\*Basic Protocol 1\*\* - Cross-validation and OOD analysis.

&#x20; - `bp2\_equity.ipynb`: \*\*Basic Protocol 2\*\* - Subgroup disparity and harm audit.

&#x20; - `bp3\_stability.ipynb`: \*\*Basic Protocol 3\*\* - Feature selection and prediction robustness.



\## 🚀 Workflow

1\. Use root \*\*SP1-2\*\* to profile your data.

2\. Use root \*\*SP3-4\*\* to generate your audit instructions.

3\. Refer to `/examples/tcga\_luad/` notebooks (\*\*BP1-3\*\*) to execute the audits.



