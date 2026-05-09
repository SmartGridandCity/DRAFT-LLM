import json
from jinja2 import Template

# Mock SP2 Statistics Card
sp2_data = {
    "study_name": "TCGA-LUAD-Audit",
    "stats": {
        "imbalance_flag": True,
        "min_class_pct": 12,
        "is_time_series": False,
        "missingness_pct": 25,
        "has_multimodal_leakage": True  # A rule-based system won't know what to do with this
    }
}

def run_rule_based(data):
    with open("templates/generalization_plan.j2") as f:
        template = Template(f.read())
    return template.render(data)

def simulate_llm_response(data):
    # This represents what DRAFT-LLM provides beyond the rules
    return """
### DRAFT-LLM ADAPTIVE PLAN
Analysis: Strategic refinement for TCGA-LUAD.

[1] EVALUATION DESIGN: 
- Strategy: Group-Stratified 5-Fold CV (Grouping by 'center_id').
- Reasoning: While imbalanced, the primary risk is batch effects from multiple sequencing centers. Simple StratifiedCV will overestimate performance.

[2] DATA HANDLING:
- Action: Modality-Specific Dropout (not Imputation).
- Reasoning: 25% missingness is concentrated in the Imaging block. Imputation will introduce artifacts; DRAFT recommends treating Imaging as an optional modality.
"""

if __name__ == "__main__":
    baseline = run_rule_based(sp2_data)
    adaptive = simulate_llm_response(sp2_data)
    
    print("--- RULE-BASED OUTPUT ---")
    print(baseline)
    print("\n--- DRAFT-LLM OUTPUT ---")
    print(adaptive)
