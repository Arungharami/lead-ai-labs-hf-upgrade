# Lead.AI Labs — Hugging Face Safe Deployment & Upload Commands

This guide provides safe, tested, credential-free command-line scripts to create, upload, and synchronize all upgraded model cards, dataset cards, synthetic CSV files, and Space demo source files to [Hugging Face](https://huggingface.co/lead-ai-labs).

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
# Create Model Repository
huggingface-cli repo create fraud-detection-xai --type model --organization lead-ai-labs || true

# Create Dataset Repositories
huggingface-cli repo create fraud-detection-Table-data --type dataset --organization lead-ai-labs || true
huggingface-cli repo create fraud-detection-sample-data --type dataset --organization lead-ai-labs || true

# Create Gradio Space Repository
huggingface-cli repo create lead-ai-fraud-shield-demo --type space --space-sdk gradio --organization lead-ai-labs || true
```

---

## 🤖 3. Model Card Upload (`lead-ai-labs/fraud-detection-xai`)

```bash
# Upload Model Card README
huggingface-cli upload lead-ai-labs/fraud-detection-xai \
  ./models/fraud-detection-xai/README.md README.md \
  --repo-type model
```

---

## 📊 4. Dataset & CSV Uploads

### A. Training Table Dataset (`lead-ai-labs/fraud-detection-Table-data`)

```bash
# Upload Dataset Card README
huggingface-cli upload lead-ai-labs/fraud-detection-Table-data \
  ./datasets/fraud-detection-Table-data/README.md README.md \
  --repo-type dataset

# Upload Synthetic CSV File (105 rows)
huggingface-cli upload lead-ai-labs/fraud-detection-Table-data \
  ./datasets/fraud-detection-Table-data/train.csv train.csv \
  --repo-type dataset
```

### B. Sample Dataset (`lead-ai-labs/fraud-detection-sample-data`)

```bash
# Upload Sample Dataset Card README
huggingface-cli upload lead-ai-labs/fraud-detection-sample-data \
  ./datasets/fraud-detection-sample-data/README.md README.md \
  --repo-type dataset

# Upload Synthetic Sample CSV File (25 rows)
huggingface-cli upload lead-ai-labs/fraud-detection-sample-data \
  ./datasets/fraud-detection-sample-data/sample_data.csv sample_data.csv \
  --repo-type dataset
```

---

## 🖥️ 5. Space Demo Source Deployment (`lead-ai-labs/lead-ai-fraud-shield-demo`)

```bash
# Upload Space Metadata Card
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/README.md README.md \
  --repo-type space

# Upload Gradio Interactive Application
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/app.py app.py \
  --repo-type space

# Upload Python Dependencies
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/requirements.txt requirements.txt \
  --repo-type space
```

---

## 💻 6. GitHub Remote Sync

```bash
# Push committed local control center changes to remote GitHub repo
git push origin main
```
