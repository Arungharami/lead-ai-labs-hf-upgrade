# Lead.AI Labs — Hugging Face Safe Deployment & Upload Commands

This guide provides safe, tested, credential-free command-line scripts to create, upload, and synchronize all upgraded model cards, dataset cards, synthetic CSV files, and Space demo source files to [Hugging Face](https://huggingface.co/lead-ai-labs) and [Arun Gharami's HF Profile](https://huggingface.co/arun-gharami).

> ⚠️ **SECURITY MANDATE:** Never hard-code private tokens in scripts or check them into Git. Always export your Hugging Face write token as an environment variable (`HF_TOKEN`).

---

## 🔑 1. Terminal Setup & Authentication

Run these commands in your local Mac shell:

```bash
# 1. Navigate to your local control center repository
cd /Users/arun/Documents/Lead-ai-labs-hf-upgrade/lead-ai-labs-hf-upgrade

# 2. Export your Hugging Face Write Token (Replace placeholder in shell, never commit!)
export HF_TOKEN="your_huggingface_write_token_here"

# 3. Verify huggingface_hub installation & authenticate
pip install --upgrade huggingface_hub
huggingface-cli login --token $HF_TOKEN
```

---

## 🏗️ 2. Repository Initialization (If repositories do not exist on HF yet)

```bash
# Organization Repositories (lead-ai-labs)
huggingface-cli repo create fraud-detection-xai --type model --organization lead-ai-labs || true
huggingface-cli repo create fraud-detection-Table-data --type dataset --organization lead-ai-labs || true
huggingface-cli repo create fraud-detection-sample-data --type dataset --organization lead-ai-labs || true
huggingface-cli repo create lead-ai-fraud-shield-demo --type space --space-sdk gradio --organization lead-ai-labs || true

# User Profile Repositories (arun-gharami)
huggingface-cli repo create lead-ai-fraud-shield --type model || true
huggingface-cli repo create lead-ai-fraud-detection-model --type model || true
huggingface-cli repo create lead-ai-customer-predictor --type model || true
huggingface-cli repo create lead-ai-review-sentinel --type model || true
huggingface-cli repo create lead-ai-fraud-detection-dataset-v2 --type dataset || true
huggingface-cli repo create lead-ai-fraud-detection-dataset --type dataset || true
huggingface-cli repo create fraud-detection-xai-demo --type space --space-sdk gradio || true
```

---

## 🤖 3. Model Card Uploads

```bash
# 1. Flagship Lead.AI Fraud Shield Model (lead-ai-labs & arun-gharami)
huggingface-cli upload lead-ai-labs/fraud-detection-xai ./models/fraud-detection-xai/README.md README.md --repo-type model
huggingface-cli upload arun-gharami/lead-ai-fraud-shield ./models/fraud-detection-xai/README.md README.md --repo-type model

# 2. Lead.AI Fraud Detection Model
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-model ./models/lead-ai-fraud-detection-model/README.md README.md --repo-type model

# 3. Lead.AI Customer Predictor (CLV & Churn Analytics)
huggingface-cli upload arun-gharami/lead-ai-customer-predictor ./models/lead-ai-customer-predictor/README.md README.md --repo-type model

# 4. Lead.AI Review Sentinel (NLP Sentiment & Spam Detection)
huggingface-cli upload arun-gharami/lead-ai-review-sentinel ./models/lead-ai-review-sentinel/README.md README.md --repo-type model
```

---

## 📊 4. Dataset & CSV Uploads

### A. Training Table Dataset v2 (`lead-ai-labs/fraud-detection-Table-data` & `arun-gharami/lead-ai-fraud-detection-dataset-v2`)

```bash
# Upload to lead-ai-labs org
huggingface-cli upload lead-ai-labs/fraud-detection-Table-data ./datasets/fraud-detection-Table-data/README.md README.md --repo-type dataset
huggingface-cli upload lead-ai-labs/fraud-detection-Table-data ./datasets/fraud-detection-Table-data/train.csv train.csv --repo-type dataset

# Upload to arun-gharami user profile
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-dataset-v2 ./datasets/fraud-detection-Table-data/README.md README.md --repo-type dataset
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-dataset-v2 ./datasets/fraud-detection-Table-data/train.csv train.csv --repo-type dataset
```

### B. Sample Dataset v1 (`lead-ai-labs/fraud-detection-sample-data` & `arun-gharami/lead-ai-fraud-detection-dataset`)

```bash
# Upload to lead-ai-labs org
huggingface-cli upload lead-ai-labs/fraud-detection-sample-data ./datasets/fraud-detection-sample-data/README.md README.md --repo-type dataset
huggingface-cli upload lead-ai-labs/fraud-detection-sample-data ./datasets/fraud-detection-sample-data/sample_data.csv sample_data.csv --repo-type dataset

# Upload to arun-gharami user profile
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-dataset ./datasets/lead-ai-fraud-detection-dataset/README.md README.md --repo-type dataset
```

---

## 🖥️ 5. Space Demo Source Deployment

```bash
# 1. Upload to lead-ai-labs Space
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo ./spaces/lead-ai-fraud-shield-demo/README.md README.md --repo-type space
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo ./spaces/lead-ai-fraud-shield-demo/app.py app.py --repo-type space
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo ./spaces/lead-ai-fraud-shield-demo/requirements.txt requirements.txt --repo-type space

# 2. Upload to arun-gharami Space
huggingface-cli upload arun-gharami/fraud-detection-xai-demo ./spaces/fraud-detection-xai-demo/README.md README.md --repo-type space
huggingface-cli upload arun-gharami/fraud-detection-xai-demo ./spaces/lead-ai-fraud-shield-demo/app.py app.py --repo-type space
huggingface-cli upload arun-gharami/fraud-detection-xai-demo ./spaces/lead-ai-fraud-shield-demo/requirements.txt requirements.txt --repo-type space
```

---

## 💻 6. GitHub Remote Sync

```bash
# Push committed local control center changes to remote GitHub repo
git push origin main
```
