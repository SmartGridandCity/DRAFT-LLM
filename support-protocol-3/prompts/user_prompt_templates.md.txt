# User Prompt Templates (Support Protocol 3)

These short prompts are generic but parameterized by the configuration.
They are intended to be used together with the system prompt produced
from the configuration.

---

## 1. EDA prompt

> Using the current configuration, propose an initial exploratory data analysis (EDA) plan for this study. Explicitly reference any data risk flags (e.g., imbalance, missingness, heterogeneity) and suggest checks that align with the stated governance and resource constraints.

---

## 2. Modeling prompt

> Propose baseline and candidate models consistent with the configuration, including preprocessing steps and evaluation strategies. Your suggestions should:
> - Respect the declared study goal and intended use.
> - Align with the user's expertise and preferred programming language.
> - Account for the data risk flags (e.g., outcome imbalance, small subgroups).
> - Stay within the allowed libraries and compute budget.

---

## 3. Robustness prompt

> Describe robustness checks and diagnostics appropriate for the study, given the configuration and the statistics card. Cover aspects such as:
> - Overfitting and generalization (e.g., resampling, permutation tests).
> - Fairness and subgroup performance, especially along sensitive attributes.
> - Stability of key features or patterns.
> Explain how each proposed check relates to the dataset's empirical properties.
