# Lead.AI Fraud Shield — Kaggle, Hugging Face and GitHub Benchmark System

This module converts the existing Lead.AI fraud demo into a reproducible ML and AI-evaluation system. It is designed for research demonstration, portfolio evidence and controlled prototyping—not autonomous financial decision-making.

## What is included

1. **Reproducible tabular training** with deterministic seeds and strict schema validation.
2. **Model selection** between balanced logistic regression and random forest using out-of-fold PR-AUC.
3. **Three-way holdout**: train, validation and untouched test sets.
4. **Fraud-aware metrics**: PR-AUC, ROC-AUC, recall, precision, F1, MCC, calibration, recall at 1% FPR and latency.
5. **Portable artifact**: `model.joblib`, `metrics.json` and `feature_schema.json`.
6. **Kaggle Community Benchmark task** for structured, grounded fraud-risk reasoning by LLMs.
7. **GitHub Actions quality gates** and a controlled Hugging Face publishing workflow.

## Local verification

```bash
python -m pip install -e ".[dev]"
pytest
python scripts/train_and_evaluate.py \
  --source synthetic \
  --synthetic-rows 5000 \
  --output-dir artifacts/fraud-detection-xai
```

To train against the repository CSV:

```bash
python scripts/train_and_evaluate.py \
  --source csv \
  --data-path datasets/fraud-detection-Table-data/train.csv
```

The current small repository CSV is suitable for smoke testing only. It is not large or independent enough to support production claims. For an external Kaggle dataset, download it under its own license, keep it out of Git, identify its binary target with `--target-column`, and run the same pipeline.

## Hugging Face deployment

Use a write-scoped token stored as `HF_TOKEN`; never commit it.

```bash
pip install -U huggingface_hub
hf auth login
hf repos create lead-ai-labs/fraud-detection-xai --type model --exist-ok
hf upload lead-ai-labs/fraud-detection-xai artifacts/fraud-detection-xai . --type model
```

The included manual GitHub workflow reruns tests, training and release gates before it uploads the model bundle and metrics to Hugging Face.

## Kaggle Community Benchmark

Files are under `kaggle/benchmarks/`:

- `fraud_risk_reasoning.py`: objective task and assertions.
- `eval_cases.csv`: auditable evaluation cases.
- `run_benchmark.py`: dataset evaluation runner.

Recommended setup:

```bash
pip install -e ".[kaggle]"
kaggle auth login
kaggle benchmarks init
python kaggle/benchmarks/run_benchmark.py
```

Then use the commands exposed by your installed Kaggle CLI:

```bash
kaggle benchmarks --help
kaggle benchmarks tasks --help
```

The benchmark grades exact JSON structure, audited decision labels, risk ranges, required evidence reason codes and avoidance of protected attributes. It does not use an LLM judge, so results are easier to reproduce.

## Data policy

- Do not claim that all Kaggle benchmark data was used; Kaggle Benchmarks contains many unrelated domains.
- Do not merge datasets with incompatible schemas without a documented adapter.
- Do not redistribute third-party datasets unless their license permits it.
- Keep a held-out test set private when publishing a serious benchmark.
- Replace synthetic quality claims with institution-specific validation before any real deployment.
