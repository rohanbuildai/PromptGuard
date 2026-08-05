"""
Hybrid decision engine.

Combines Rule Engine, Semantic Engine and
Machine Learning Engine into a final risk assessment.

"""


from .rule_engine import detect_prompt_injection
from .semantic_engine import detect_semantic_prompt_injection
from .ml_engine import detect_ml_prompt


RISK_LEVELS = {
    "SAFE": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}
LEVEL_TO_RISK = {
    0: "SAFE",
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH"
}

def analyze_prompt(prompt) :

    rule_result = detect_prompt_injection(prompt)
    semantic_result = detect_semantic_prompt_injection(prompt)
    ml_result = detect_ml_prompt(prompt)

    rule_risk = rule_result["risk"]
    semantic_risk = semantic_result["risk"]
    ml_risk = ml_result["risk"]

    rule_level = RISK_LEVELS[rule_risk]
    semantic_level = RISK_LEVELS[semantic_risk]
    ml_level = RISK_LEVELS[ml_risk]

    overall_level = max(rule_level,semantic_level,ml_level)
    overall_risk = LEVEL_TO_RISK[overall_level]

    sources = []

    if rule_level == overall_level:
        sources.append("rule_engine")

    if semantic_level == overall_level:
        sources.append("semantic_engine")

    if ml_level == overall_level:
        sources.append("ml_engine")

    decision_source = ", ".join(sources)

    decision_reason = (
    f"Final decision is {overall_risk} "
    f"based on {decision_source.replace('_', ' ')}."
)

    if overall_risk == "HIGH":
        final_recommendation = "Block this prompt before forwarding it to the LLM."

    elif overall_risk == "MEDIUM":
        final_recommendation = "Manual review recommended before forwarding."

    elif overall_risk == "LOW":
        final_recommendation = "Allow the prompt but log and monitor."

    else:
        final_recommendation = "Prompt appears safe to process."


    return {
        "overall_risk": overall_risk,

        "decision": {
            "source": "Hybrid Decision Engine",
            "reason": decision_reason,
            "recommendation": final_recommendation
        },

        "engines": {
            "rule_engine": rule_result,
            "semantic_engine": semantic_result,
            "ml_engine": ml_result
        }
    }