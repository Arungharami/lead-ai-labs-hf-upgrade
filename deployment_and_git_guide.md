# Lead.AI Labs — Verified Deployment and Release Guide

This repository is the source of truth for the Lead.AI fraud benchmark, Hugging Face assets, and Kaggle evaluation files. Releases should move through reviewed GitHub changes and automated verification rather than direct untracked uploads.

## Release architecture

```text
GitHub source and review
        │
        ├── Fraud Benchmark CI
        │     ├── package installation
        │     ├── automated tests
        │     ├── reproducible model training
        │     ├── held-out quality gates
        │     └── model artifact upload
        │
        ├── Hugging Face release workflow
        │     ├── rerun tests and gates
        │     └── upload model, metrics, schema and card
        │
        └── Kaggle Benchmarks
              ├── objective fraud-reasoning task
              ├── audited evaluation cases
              └── leaderboard run files
```

## GitHub workflow

Create a branch, validate locally, open a pull request, and merge only after checks pass.

```bash
git checkout -b feature/<descriptive-name>
python -m pip install -e ".[dev]"
pytest
python scripts/train_and_evaluate.py --source synthetic --synthetic-rows 5000 --seed 42
git add .
git commit -m "feat: describe the verified change"
git push -u origin feature/<descriptive-name>
```

Do not commit generated tokens, `kaggle.json`, `.env` files, local caches, or third-party datasets that cannot legally be redistributed.

## Hugging Face release

The preferred path is the protected manual workflow:

1. Add a write-scoped `HF_TOKEN` secret to the GitHub environment named `huggingface-production`.
2. Run **Publish Verified Model to Hugging Face** from GitHub Actions.
3. Select the approved training source.
4. Confirm the workflow passes tests and release gates.
5. Verify the Hub model repository contains `model.joblib`, `metrics.json`, `feature_schema.json`, and the current model card.

Current CLI equivalents are documented in `upload_commands.md`. Use the `hf` command, not the deprecated `huggingface-cli` command.

## Kaggle Benchmarks release

Install and authenticate the current Kaggle CLI in a secure local or CI environment:

```bash
python -m pip install -e ".[kaggle]"
kaggle auth login
kaggle benchmarks --help
kaggle benchmarks tasks --help
python kaggle/benchmarks/run_benchmark.py
```

The task source is `kaggle/benchmarks/fraud_risk_reasoning.py`; audited cases are in `kaggle/benchmarks/eval_cases.csv`. Use the exact push/run syntax shown by the installed CLI because command details can change between versions.

For legacy Kaggle datasets and notebooks, keep their metadata files beside the assets and use:

```bash
kaggle datasets create -p kaggle/fraud-detection-table-data
kaggle datasets create -p kaggle/fraud-detection-sample-data
kaggle kernels push -p kaggle/notebooks
```

Use version/update commands instead of `create` when an asset already exists.

## Website integration

The website should link only to assets that are live and verified. Before publishing a product page, check that:

- the GitHub default branch contains the referenced implementation;
- the Hugging Face model repository contains the actual serialized artifact, not only a card;
- the dataset card reports the correct 105-row `n<1K` size and smoke-test scope;
- the Kaggle benchmark or notebook is publicly accessible; and
- the Gradio Space status is healthy if it is advertised as live.

Do not describe the existing rule-based Space as the trained model until it loads the verified model bundle.

## Release checklist

- [ ] Pull request reviewed and merged.
- [ ] `Fraud Benchmark CI` succeeded.
- [ ] Metrics are generated from an untouched test partition.
- [ ] Synthetic results are labeled as synthetic.
- [ ] Model and dataset cards match the artifacts.
- [ ] No unsupported SHAP/LIME, production, or accuracy claims remain.
- [ ] License and provenance are documented for every dataset.
- [ ] Hugging Face token and Kaggle credentials remain secret.
- [ ] Hub and Kaggle links are manually verified after publishing.
- [ ] Downstream demos pin a trusted model revision.

## Current positioning

Lead.AI Fraud Shield is a reproducible, research-oriented fraud-risk baseline and AI evaluation project. It demonstrates professional engineering practices across GitHub, Hugging Face, and Kaggle, but it must not be represented as a production financial decision system without representative institutional data, governance, monitoring, security review, and human oversight.
