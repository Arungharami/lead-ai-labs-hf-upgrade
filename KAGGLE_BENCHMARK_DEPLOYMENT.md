# Lead.AI Kaggle Benchmark Deployment

Live benchmark:

`https://www.kaggle.com/benchmarks/arungharami/lead-ai-fraud-risk-reasoning-benchmark/leaderboard`

## Benchmark task suite

| Task slug | Capability | Cases | Score |
|---|---|---:|---:|
| `lead-ai-fraud-policy-reasoning` | Deterministic policy application, JSON compliance, scoring, reason codes, protected-attribute avoidance | 15 balanced cases | 0.0-1.0 |
| `lead-ai-fraud-adversarial-safety` | Prompt-injection resistance, identity-pressure resistance, trusted-signal use | 8 adversarial cases | 0.0-1.0 |
| `lead-ai-fraud-uncertainty-escalation` | Missing/invalid input detection, non-fabrication, human escalation | 8 incomplete-data cases | 0.0-1.0 |

All expected results are computed deterministically. The benchmark does not use an LLM judge.

## Secure automated publication

1. Open the GitHub repository settings.
2. Create an environment named `kaggle-production`.
3. Add an environment secret named `KAGGLE_API_TOKEN` using a token generated from Kaggle account settings.
4. Do not paste the token into source code, issues, notebooks, or chat messages.
5. Open **Actions → Publish Kaggle Benchmark Suite → Run workflow**.
6. Keep the default model list or enter current model slugs returned by:

```bash
kaggle b t models
```

The workflow performs the following operations:

- installs the official Kaggle CLI;
- runs the repository benchmark contract tests;
- creates or versions all three tasks;
- waits for server-side task creation;
- publishes each task and its backing notebook;
- runs each task against the selected models;
- prints task status and the benchmark leaderboard.

## Attach the tasks to the benchmark

Kaggle currently manages benchmark collections through its web editor. After the workflow publishes the tasks:

1. Open the benchmark page while signed in as `arungharami`.
2. Select **Edit benchmark** or **Add tasks**.
3. Add these public tasks:
   - `arungharami/lead-ai-fraud-policy-reasoning`
   - `arungharami/lead-ai-fraud-adversarial-safety`
   - `arungharami/lead-ai-fraud-uncertainty-escalation`
4. Keep the task order shown above.
5. Save and publish the benchmark version.
6. Return to the leaderboard. Completed model runs should appear as rows, with the three tasks as columns.

## Recommended benchmark description

> A deterministic evaluation suite for fraud-risk reasoning, prompt-injection resistance, and uncertainty-aware human escalation. Models must apply a disclosed numeric policy, return strict auditable JSON, ground decisions in trusted transaction signals, avoid protected-attribute reasoning, and refuse to invent missing values.

## Verification commands

```bash
kaggle b t status lead-ai-fraud-policy-reasoning
kaggle b t status lead-ai-fraud-adversarial-safety
kaggle b t status lead-ai-fraud-uncertainty-escalation
kaggle b leaderboard arungharami/lead-ai-fraud-risk-reasoning-benchmark --show
```

## Interpretation

Scores are controlled benchmark results, not evidence of production fraud-detection performance. The tasks evaluate instruction following, policy arithmetic, structured output, safety, and escalation behavior on synthetic evaluation cases. They do not establish regulatory compliance, real-world calibration, or deployment readiness by themselves.
