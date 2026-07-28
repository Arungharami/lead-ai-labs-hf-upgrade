"""Run the complete Lead.AI fraud benchmark suite in a Kaggle environment."""

import kaggle_benchmarks as kbench

from fraud_adversarial_safety import fraud_adversarial_safety
from fraud_risk_reasoning import fraud_policy_reasoning
from fraud_uncertainty_escalation import fraud_uncertainty_escalation

TASKS = (
    fraud_policy_reasoning,
    fraud_adversarial_safety,
    fraud_uncertainty_escalation,
)

for task in TASKS:
    run = task.run(kbench.llm)
    print(run)
