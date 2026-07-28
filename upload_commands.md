# Lead.AI Labs — Current Hugging Face Deployment Guide

This guide uses the current `hf` CLI. The older `huggingface-cli` command is deprecated and should not be used in new automation.

## Security rules

- Create a write-scoped Hugging Face token with only the permissions required for the target repositories.
- Store the token in your shell or the GitHub `huggingface-production` environment as `HF_TOKEN`.
- Never commit a token, `kaggle.json`, or generated credential file.
- Prefer the gated GitHub workflow in `.github/workflows/publish-huggingface.yml` for the verified fraud-model release.

## Install and authenticate

```bash
python -m pip install --upgrade huggingface_hub
hf version
hf auth login
hf auth whoami
```

For non-interactive automation, set `HF_TOKEN` in the execution environment instead of writing it in a command or file.

## Create repositories safely

```bash
hf repos create lead-ai-labs/fraud-detection-xai --type model --exist-ok
hf repos create lead-ai-labs/fraud-detection-Table-data --type dataset --exist-ok
hf repos create lead-ai-labs/fraud-detection-sample-data --type dataset --exist-ok
hf repos create lead-ai-labs/lead-ai-fraud-shield-demo --type space --space-sdk gradio --exist-ok
```

Create additional user-profile repositories only when they serve a distinct maintained purpose. Avoid duplicating identical artifacts across many repositories because copies drift and confuse users.

## Publish the verified fraud model

First generate and test the artifact:

```bash
python -m pip install -e ".[dev,huggingface]"
pytest
python scripts/train_and_evaluate.py \
  --source synthetic \
  --synthetic-rows 10000 \
  --seed 42 \
  --output-dir artifacts/fraud-detection-xai
```

Then upload the generated bundle and current model card:

```bash
hf upload lead-ai-labs/fraud-detection-xai \
  artifacts/fraud-detection-xai . \
  --type model \
  --commit-message "Publish verified fraud model and metrics"

hf upload lead-ai-labs/fraud-detection-xai \
  models/fraud-detection-xai/README.md README.md \
  --type model \
  --commit-message "Update auditable model card"
```

## Publish the 105-row smoke-test dataset

```bash
hf upload lead-ai-labs/fraud-detection-Table-data \
  datasets/fraud-detection-Table-data . \
  --type dataset \
  --commit-message "Update synthetic smoke-test dataset and card"
```

Do not describe this 105-row file as a production corpus or independent benchmark.

## Publish the sample dataset

```bash
hf upload lead-ai-labs/fraud-detection-sample-data \
  datasets/fraud-detection-sample-data . \
  --type dataset \
  --commit-message "Update sample fraud dataset"
```

## Publish the Gradio Space source

```bash
hf upload lead-ai-labs/lead-ai-fraud-shield-demo \
  spaces/lead-ai-fraud-shield-demo . \
  --type space \
  --commit-message "Update fraud demo Space"
```

The existing Space application is a transparent rule-based demonstration. Do not describe it as the serialized trained model until the application is changed to download and run the verified model bundle.

## Verify each publication

```bash
hf models info lead-ai-labs/fraud-detection-xai
hf datasets info lead-ai-labs/fraud-detection-Table-data
hf spaces info lead-ai-labs/lead-ai-fraud-shield-demo
```

For model loading, pin a trusted Hub revision and review the Hub security scan before loading `model.joblib`, because joblib uses pickle-compatible serialization.

## Preferred GitHub release path

1. Merge only after `Fraud Benchmark CI` passes.
2. Add `HF_TOKEN` to the protected `huggingface-production` GitHub environment.
3. Run **Publish Verified Model to Hugging Face** manually.
4. Confirm `model.joblib`, `metrics.json`, `feature_schema.json`, and the corrected `README.md` appear in the model repository.
5. Record the Hub commit SHA used by demos and downstream services.
