---
license: cc-by-4.0
task_categories:
- tabular-classification
language:
- en
tags:
- fraud-detection
- explainable-ai
- financial-ai
- risk-scoring
- trustworthy-ai
- synthetic-data
- lead-ai
pretty_name: Lead.AI Fraud Detection Table Data
size_categories:
- n<1K
---

# Lead.AI Fraud Detection Table Data

`lead-ai-labs/fraud-detection-Table-data` contains **105 synthetic transaction-style rows** for software smoke tests, schema demonstrations, classroom examples, and early fraud-classification prototypes.

It contains no real customer records, payment credentials, card numbers, bank data, or personally identifiable information.

## Important scope

This file is intentionally small. It is **not** a production training corpus, an independent research benchmark, or evidence of real-world fraud-model performance. A random train/test split of 105 closely structured synthetic rows can produce unstable or misleading results.

For reproducible model evaluation, use the larger probabilistic generator and held-out protocol in the associated GitHub repository:

```bash
python scripts/train_and_evaluate.py \
  --source synthetic \
  --synthetic-rows 5000 \
  --seed 42
```

## Dataset facts

| Property | Value |
|---|---|
| File | `train.csv` |
| Rows | 105 |
| Format | CSV |
| Target | `is_fraud` |
| Labels | `0` legitimate-style, `1` fraud-style |
| Data origin | Synthetic transaction-style examples |
| Intended use | Smoke testing, education, prototyping |
| License | CC BY 4.0 |

Users should calculate the current class distribution directly from the file rather than assuming that it is balanced.

## Load from Hugging Face

```python
from datasets import load_dataset

dataset = load_dataset("lead-ai-labs/fraud-detection-Table-data")
df = dataset["train"].to_pandas()

print(df.shape)
print(df["is_fraud"].value_counts(dropna=False))
print(df.head())
```

## Column schema

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | Synthetic record identifier; exclude from model features |
| `amount` | float | Transaction amount |
| `transaction_hour` | integer | Hour from 0 to 23 |
| `merchant_risk_score` | float | Synthetic merchant-risk signal |
| `customer_age_days` | integer | Synthetic account tenure |
| `device_trust_score` | float | Synthetic device-trust signal |
| `location_risk_score` | float | Synthetic location-risk signal |
| `velocity_24h` | integer | Synthetic recent-attempt count |
| `previous_chargebacks` | integer | Synthetic prior-chargeback count |
| `payment_method_risk` | float | Synthetic payment-method risk signal |
| `is_fraud` | integer | Binary target |

## Data provenance and caveats

- The rows are synthetic and encode simplified relationships between transaction risk signals and labels.
- The original 105-row file predates the reproducible probabilistic generator now included in the engineering repository; therefore, do not describe this file as empirically calibrated unless separate provenance evidence is added.
- `transaction_id` is an identifier and should not be used as a predictive feature.
- The dataset does not include protected attributes and cannot support a meaningful fairness audit.
- Results from this file should be labeled as smoke-test or demonstration results.
- Do not combine this dataset with unrelated Kaggle or Hugging Face datasets without documenting schema mapping, license compatibility, duplicate handling, leakage checks, and split strategy.

## Responsible use

Appropriate uses include validating data loaders, testing UI flows, demonstrating feature schemas, and teaching binary classification. Unsupported uses include production fraud accusations, automated account blocking, credit decisions, compliance conclusions, or claims about real populations.

## Related implementation

The associated engineering repository provides:

- schema and leakage validation;
- a reproducible synthetic generator;
- cross-validated model selection;
- train/validation/untouched-test evaluation;
- Kaggle Community Benchmark tasks;
- GitHub Actions quality gates; and
- controlled Hugging Face publishing.

See `BENCHMARKS.md` in `Arungharami/lead-ai-labs-hf-upgrade` for operating instructions.

## Citation

```bibtex
@dataset{gharami_lead_ai_fraud_table_data_2026,
  author = {Arun Kumar Gharami},
  title = {Lead.AI Fraud Detection Table Data},
  year = {2026},
  publisher = {Lead.AI Labs},
  url = {https://huggingface.co/datasets/lead-ai-labs/fraud-detection-Table-data}
}
```
