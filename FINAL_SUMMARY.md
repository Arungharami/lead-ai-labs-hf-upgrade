# Lead.AI Labs — Verified Kaggle, Hugging Face and GitHub Upgrade Summary

## Result

The Lead.AI fraud portfolio has been upgraded from documentation and a rule-based demonstration into a reproducible engineering and evaluation system.

The default branch now provides:

- a Python 3.11 package for data validation, model selection, evaluation, serialization, and inference support;
- balanced logistic-regression and random-forest candidates selected by out-of-fold PR-AUC;
- separate training, validation, and untouched-test partitions;
- validation-only decision-threshold selection;
- fraud-relevant performance, calibration, confusion-matrix, and latency metrics;
- objective Kaggle Community Benchmark tasks and audited evaluation cases;
- a verified Kaggle notebook that runs the real pipeline instead of displaying hardcoded metrics;
- GitHub Actions tests and minimum release gates;
- a protected Hugging Face publishing workflow using the current `hf` CLI;
- corrected model and dataset cards with accurate provenance, size, limitations, and measured results; and
- responsible-use and deployment documentation.

## Reproducible CI reference result

The controlled reference run uses 5,000 probabilistic synthetic transactions, seed 42, and a 60/20/20 split. Balanced logistic regression is selected on the training partition.

| Untouched-test metric | Result |
|---|---:|
| ROC-AUC | 0.9021 |
| PR-AUC | 0.5845 |
| Recall | 0.7952 |
| Precision | 0.3028 |
| F1 | 0.4385 |
| Balanced accuracy | 0.8147 |
| MCC | 0.4206 |
| Brier score | 0.1165 |

These results are synthetic benchmark results and must not be represented as production, institutional, customer, or regulatory performance.

## Data status

The repository contains a 105-row synthetic transaction CSV and a smaller sample file. The 105-row file is now correctly documented as `n<1K` and suitable only for schema checks, UI testing, education, and smoke tests.

The two existing datasets have incompatible schemas and are not merged blindly. Third-party Kaggle or Hugging Face datasets must be handled through documented adapters, license checks, leakage controls, and independent splits.

## Platform status

### GitHub

The complete source, tests, workflows, notebook, benchmark task, and documentation are maintained in `Arungharami/lead-ai-labs-hf-upgrade`.

### Hugging Face

The verified release workflow is ready to upload:

- `model.joblib`;
- `metrics.json`;
- `feature_schema.json`; and
- the corrected model card.

A write-scoped `HF_TOKEN` must be stored in the protected GitHub environment `huggingface-production`. A Hugging Face page containing only a README is documentation-only and must not be described as a deployed trained model.

The existing Gradio source is a transparent rule-based demonstration. It is not yet the serialized model and should not be marketed as such until it downloads and runs a pinned verified model artifact.

### Kaggle

The repository now contains two Kaggle layers:

1. A Community Benchmark task for structured fraud-risk reasoning with objective assertions.
2. A verified notebook that performs reproducible tabular model selection and held-out evaluation.

Live publishing requires authenticated Kaggle access. Use the exact commands exposed by the current installed Kaggle CLI.

## Removed or corrected claims

- Unsupported 94.2% accuracy and 0.963 ROC-AUC claims were removed.
- The model is no longer described as a gradient-boosted SHAP/LIME artifact without evidence.
- The model card explicitly states that per-record SHAP/LIME is not yet bundled.
- The tiny CSV is no longer described as a large, balanced, empirically calibrated benchmark.
- Deprecated `huggingface-cli` instructions were replaced by the current `hf` CLI.
- The Kaggle notebook no longer uses hardcoded performance claims.

## Required final publication actions

1. Add the secure Hugging Face token to the protected GitHub environment.
2. Run **Publish Verified Model to Hugging Face**.
3. Authenticate the Kaggle CLI and push the benchmark/notebook assets.
4. Verify every public link and artifact after publishing.
5. Pin downstream demos to a trusted Hub commit SHA.

## Positioning

Lead.AI Fraud Shield is now a professional, reproducible research baseline and multi-platform AI evaluation project. It demonstrates strong software engineering and trustworthy-ML practices, but production deployment still requires representative institutional data, calibration, drift and fairness monitoring, security and compliance review, incident response, and human oversight.
