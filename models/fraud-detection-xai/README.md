---
license: mit
library_name: scikit-learn
pipeline_tag: tabular-classification
tags:
- fraud-detection
- financial-risk
- tabular-classification
- explainable-ai
- synthetic-data
- trustworthy-ai
- lead-ai
---

# Lead.AI Fraud Shield — Auditable Fraud-Risk Baseline

`lead-ai-labs/fraud-detection-xai` is a reproducible scikit-learn baseline for binary transaction-fraud risk research. The release is built by the source-controlled pipeline in `Arungharami/lead-ai-labs-hf-upgrade` and is intended for research demonstrations, portfolio evidence, benchmarking, and controlled prototyping.

It is **not** a production fraud service, a credit-scoring system, or an autonomous adverse-action system.

## Release status

The verified publishing workflow uploads these files after tests and release gates pass:

- `model.joblib` — fitted estimator, feature order, operating threshold, candidate scores, and provenance metadata.
- `metrics.json` — validation and untouched-test metrics.
- `feature_schema.json` — required feature names and target information.
- `README.md` — this model card.

A Hub page that contains only this card and not the three generated artifacts is documentation-only and should not be represented as a deployed trained model.

## Model-development process

The pipeline evaluates two class-imbalance-aware candidates:

1. Standardized logistic regression with balanced class weights.
2. Random forest with balanced subsampling.

Candidate selection uses out-of-fold precision-recall AUC on the training partition. The selected estimator is refitted on all training rows. The decision threshold is chosen on a separate validation partition to satisfy a requested minimum recall while maximizing precision. Final metrics are calculated once on an untouched test partition.

For the reproducible CI benchmark below, balanced logistic regression was selected.

## Reproducible synthetic benchmark

| Item | Value |
|---|---:|
| Generator | Lead.AI probabilistic synthetic transaction generator |
| Rows | 5,000 |
| Random seed | 42 |
| Split | 60% train / 20% validation / 20% untouched test |
| Test rows | 1,000 |
| Test fraud prevalence | 8.3% |
| Validation-selected threshold | 0.4928 |

### Untouched-test results

| Metric | Result |
|---|---:|
| PR-AUC | 0.5845 |
| ROC-AUC | 0.9021 |
| Balanced accuracy | 0.8147 |
| Recall | 0.7952 |
| Precision | 0.3028 |
| F1 | 0.4385 |
| Matthews correlation coefficient | 0.4206 |
| Brier score | 0.1165 |
| Expected calibration error | 0.1735 |
| Recall at 1% maximum FPR | 0.3614 |
| Confusion matrix | TN 765 / FP 152 / FN 17 / TP 66 |

These results measure a controlled **synthetic** benchmark, not real-world or institutional performance. The recall-oriented operating threshold intentionally accepts more false positives; organizations must choose thresholds using their own loss costs, review capacity, prevalence, and compliance requirements.

## Input schema

| Feature | Type | Meaning |
|---|---|---|
| `amount` | float | Transaction amount |
| `transaction_hour` | integer, 0–23 | Local transaction hour |
| `merchant_risk_score` | float, 0–1 | Merchant-category risk signal |
| `customer_age_days` | integer | Account tenure in days |
| `device_trust_score` | float, 0–1 | Device trust signal |
| `location_risk_score` | float, 0–1 | Location anomaly signal |
| `velocity_24h` | integer | Recent transaction-attempt count |
| `previous_chargebacks` | integer | Prior chargeback count |
| `payment_method_risk` | float, 0–1 | Payment-instrument risk signal |

`transaction_id` is intentionally excluded from training to reduce identifier leakage.

## Loading a verified artifact

Only load serialized model files from a repository and revision you trust. `joblib` uses pickle-compatible serialization and can execute code during loading.

```python
import joblib
import pandas as pd
from huggingface_hub import hf_hub_download

revision = "PIN_A_TRUSTED_COMMIT_SHA"
model_path = hf_hub_download(
    repo_id="lead-ai-labs/fraud-detection-xai",
    filename="model.joblib",
    revision=revision,
)
bundle = joblib.load(model_path)

record = pd.DataFrame([{
    "amount": 1250.00,
    "transaction_hour": 3,
    "merchant_risk_score": 0.85,
    "customer_age_days": 12,
    "device_trust_score": 0.15,
    "location_risk_score": 0.88,
    "velocity_24h": 14,
    "previous_chargebacks": 2,
    "payment_method_risk": 0.80,
}])

features = bundle["feature_names"]
probability = float(bundle["estimator"].predict_proba(record[features])[:, 1][0])
prediction = int(probability >= bundle["threshold"])
print({"fraud_probability": probability, "prediction": prediction})
```

## Explainability status

The current release provides an auditable feature schema, transparent candidate selection, reproducible metrics, and a linear model when logistic regression wins. A packaged per-record SHAP or LIME explanation engine is **not yet part of the verified model bundle** and should not be claimed as an available artifact until implemented and tested.

## Intended uses

- Reproducible fraud-classification research and teaching.
- CI validation of a tabular ML pipeline.
- Controlled product prototypes with human review.
- Baseline comparison before training on properly licensed, representative data.

## Prohibited or unsupported uses

- Automatic accusations, account termination, or law-enforcement reporting.
- Credit eligibility, lending, insurance pricing, or other regulated adverse decisions.
- Deployment without local validation, monitoring, human review, and incident procedures.
- Claims that synthetic results represent real customers or production traffic.

## Limitations and required validation

- Synthetic relationships may be easier, cleaner, or materially different from real fraud behavior.
- Performance can change with prevalence, geography, merchant mix, device signals, and concept drift.
- Calibration is not production-ready and must be reassessed on representative labels.
- Fairness testing requires lawful, carefully governed evaluation data and is not supplied by this synthetic benchmark.
- The small 105-row repository CSV is for smoke testing, not a defensible independent benchmark.

## Reproduction

```bash
python -m pip install -e ".[dev]"
pytest
python scripts/train_and_evaluate.py \
  --source synthetic \
  --synthetic-rows 5000 \
  --seed 42 \
  --output-dir artifacts/fraud-detection-xai
```

See `BENCHMARKS.md` in the engineering repository for Kaggle Benchmarks and Hugging Face publishing procedures.

## Citation

```bibtex
@software{gharami_lead_ai_fraud_shield_2026,
  author = {Arun Kumar Gharami},
  title = {Lead.AI Fraud Shield: Auditable Fraud-Risk Baseline},
  year = {2026},
  publisher = {Lead.AI Labs},
  url = {https://github.com/Arungharami/lead-ai-labs-hf-upgrade}
}
```
