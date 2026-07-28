# Lead.AI Labs — Fraud Benchmark, Hugging Face and Kaggle Control Center

[![Website](https://img.shields.io/badge/Website-lead--ai.us-00D2FF?style=for-the-badge&logo=google-chrome&logoColor=white)](https://www.lead-ai.us)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-lead--ai--labs-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/lead-ai-labs)
[![Kaggle](https://img.shields.io/badge/Kaggle-arungharami-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/arungharami)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

This repository is the engineering source of truth for the Lead.AI Fraud Shield research baseline and its GitHub, Hugging Face, and Kaggle assets.

It includes a reproducible tabular model pipeline, held-out evaluation, objective Kaggle Community Benchmark tasks, automated quality gates, artifact integrity checks, and controlled Hugging Face publishing. It also retains the associated dataset cards, demo assets, notebooks, and portfolio materials.

## Verified status

- **GitHub implementation:** merged, pull-request reviewed, and CI-tested.
- **Model training:** balanced logistic regression and random forest candidates selected by out-of-fold PR-AUC.
- **Evaluation:** train, validation, and untouched-test partitions; threshold selected on validation only.
- **Runtime:** Python 3.11 with scikit-learn 1.9.0 pinned for model-bundle portability.
- **Artifact integrity:** runtime provenance and SHA-256 checksums generated for every release.
- **Kaggle Benchmarks:** structured fraud-risk reasoning task with objective assertions and audited cases.
- **Hugging Face publishing:** protected manual workflow requiring a write-scoped `HF_TOKEN`.
- **105-row CSV:** synthetic smoke-test data only; not a production corpus or independent benchmark.
- **Existing Gradio app:** transparent rule-based demonstration; not yet the serialized trained model.

## Reproducible synthetic benchmark

The CI reference run uses 5,000 probabilistic synthetic transactions with seed 42 and a 60/20/20 split.

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

These are controlled synthetic results, not real-world or institutional performance claims.

## Repository map

```text
lead-ai-labs-hf-upgrade/
├── src/lead_ai_bench/                  # Data, model selection and evaluation package
├── scripts/train_and_evaluate.py       # Reproducible train/validation/test pipeline
├── tests/                              # End-to-end automated verification
├── kaggle/benchmarks/                  # Kaggle Community Benchmark task and cases
├── models/fraud-detection-xai/         # Auditable Hugging Face model card
├── datasets/                           # Synthetic dataset cards and CSV assets
├── spaces/                             # Gradio demo source
├── .github/workflows/
│   ├── benchmark-ci.yml                # Test, train, verify and upload CI artifact
│   └── publish-huggingface.yml         # Protected verified Hub release
├── BENCHMARKS.md                       # Complete benchmark operating guide
├── upload_commands.md                  # Current `hf` CLI commands
└── deployment_and_git_guide.md         # Reviewed release process
```

## Local quickstart

Python 3.11 or newer is required. The project pins scikit-learn 1.9.0 because joblib model bundles are not guaranteed to be portable across scikit-learn versions.

```bash
python -m pip install -e ".[dev]"
pytest
python scripts/train_and_evaluate.py \
  --source synthetic \
  --synthetic-rows 5000 \
  --seed 42 \
  --output-dir artifacts/fraud-detection-xai
```

Generated release files:

- `model.joblib` — fitted estimator and metadata bundle.
- `metrics.json` — validation and untouched-test report.
- `feature_schema.json` — ordered feature contract and target metadata.
- `runtime.json` — Python, platform, and package versions.
- `SHA256SUMS.txt` — integrity checks for the four generated artifacts.

Verify artifact integrity:

```bash
cd artifacts/fraud-detection-xai
sha256sum --check SHA256SUMS.txt
```

## Supported data inputs

```bash
# Repository CSV smoke test
python scripts/train_and_evaluate.py \
  --source csv \
  --data-path datasets/fraud-detection-Table-data/train.csv

# Hugging Face dataset adapter
python -m pip install -e ".[huggingface]"
python scripts/train_and_evaluate.py \
  --source huggingface \
  --hf-repo lead-ai-labs/fraud-detection-Table-data
```

Third-party Kaggle or Hugging Face datasets should remain under their own licenses. Do not copy or merge unrelated data blindly. Add a documented adapter, confirm license compatibility, remove duplicate leakage, and preserve an untouched test set.

The protected public-release workflow intentionally does not publish a model trained on the 105-row smoke-test CSV.

## Kaggle Community Benchmark

```bash
python -m pip install -e ".[kaggle]"
kaggle auth login
python kaggle/benchmarks/run_benchmark.py
```

The benchmark checks:

- exact JSON structure;
- audited APPROVE, REVIEW, or DECLINE decisions;
- acceptable risk-score ranges;
- required evidence reason codes; and
- avoidance of protected or sensitive attributes.

Use `kaggle benchmarks --help` and `kaggle benchmarks tasks --help` for the exact commands supported by the installed Kaggle CLI.

## Hugging Face publishing

The preferred release path is GitHub Actions: **Publish Verified Model to Hugging Face**. Add `HF_TOKEN` to the protected `huggingface-production` environment, then run the workflow manually.

The workflow reruns tests, retrains the candidate, verifies the pinned runtime, enforces minimum quality and latency gates, checks SHA-256 integrity, stores an immutable GitHub artifact, and only then uploads to Hugging Face.

Current local CLI flow:

```bash
python -m pip install --upgrade huggingface_hub
hf auth login
hf auth whoami
hf repos create lead-ai-labs/fraud-detection-xai --type model --exist-ok
hf upload lead-ai-labs/fraud-detection-xai artifacts/fraud-detection-xai . --type model
hf upload lead-ai-labs/fraud-detection-xai models/fraud-detection-xai/README.md README.md --type model
```

Only describe the Hub repository as a trained model release after `model.joblib`, `metrics.json`, `feature_schema.json`, `runtime.json`, and `SHA256SUMS.txt` are present and verified.

## Responsible use

This project is for research, education, controlled prototyping, and engineering demonstrations. It must not be used as the sole basis for fraud accusations, account blocking, credit decisions, insurance decisions, law-enforcement reporting, or other regulated adverse actions.

Real deployment requires representative labeled data, local threshold selection, calibration, drift monitoring, security review, incident response, compliance review, and human oversight.

## Lead.AI Labs

- Founder: Arun Kumar Gharami
- Focus: trustworthy AI, explainable financial risk, predictive analytics, and business automation
- Website: https://www.lead-ai.us
- Hugging Face: https://huggingface.co/lead-ai-labs
- Kaggle: https://www.kaggle.com/arungharami
