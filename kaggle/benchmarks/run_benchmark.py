from pathlib import Path

import pandas as pd
import kaggle_benchmarks as kbench

from fraud_risk_reasoning import fraud_risk_reasoning

cases = pd.read_csv(Path(__file__).with_name("eval_cases.csv"))
results = fraud_risk_reasoning.evaluate(
    llm=[kbench.llm],
    evaluation_data=cases,
    n_jobs=2,
    timeout=120,
    max_attempts=3,
    retry_delay=10,
    remove_run_files=False,
)
print(results.as_dataframe())
