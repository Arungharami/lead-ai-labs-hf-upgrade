# Lead.AI Labs — Hugging Face Safe Deployment & Upload Commands

This guide provides tested, credential-free command-line scripts to upload and synchronize all upgraded model cards, dataset cards, synthetic CSV files, and Space demo source files to [Hugging Face](https://huggingface.co/lead-ai-labs).

> ⚠️ **SECURITY MANDATE:** Never hard-code private tokens in scripts or check them into Git. Always export your Hugging Face write token as an environment variable (`HF_TOKEN`).

---

## 🔑 1. Environment Setup & Authentication

```bash
# Export your Hugging Face Write Token (Do NOT commit real tokens!)
export HF_TOKEN="your_huggingface_write_token_here"

# Install or verify huggingface_hub CLI
pip install --upgrade huggingface_hub

# Authenticate CLI
huggingface-cli login --token $HF_TOKEN
```

---

## 🤖 2. Model Card Upload (`lead-ai-labs/fraud-detection-xai`)

```bash
# Upload Model Card README
huggingface-cli upload lead-ai-labs/fraud-detection-xai \
  ./models/fraud-detection-xai/README.md README.md \
  --repo-type model
```

---

## 📊 3. Dataset Uploads

### A. Training Table Dataset (`lead-ai-labs/fraud-detection-Table-data`)

```bash
# Upload Dataset Card README
huggingface-cli upload lead-ai-labs/fraud-detection-Table-data \
  ./datasets/fraud-detection-Table-data/README.md README.md \
  --repo-type dataset

# Upload Synthetic CSV File
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

# Upload Synthetic Sample CSV File
huggingface-cli upload lead-ai-labs/fraud-detection-sample-data \
  ./datasets/fraud-detection-sample-data/sample_data.csv sample_data.csv \
  --repo-type dataset
```

---

## 🖥️ 4. Space Demo Deployment (`lead-ai-labs/lead-ai-fraud-shield-demo`)

```bash
# Option A: Upload files directly via Hugging Face CLI
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/README.md README.md \
  --repo-type space

huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/app.py app.py \
  --repo-type space

huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo \
  ./spaces/lead-ai-fraud-shield-demo/requirements.txt requirements.txt \
  --repo-type space

# Option B: Clone Space Git Repo and sync directly
# git clone https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo /tmp/space-repo
# cp ./spaces/lead-ai-fraud-shield-demo/* /tmp/space-repo/
# cd /tmp/space-repo && git add . && git commit -m "Deploy Lead.AI Fraud Shield Demo" && git push
```

---

## 💻 5. Local GitHub Repository Commit & Push

```bash
# Navigate to repo root
cd /Users/arun/Documents/Lead-ai-labs-hf-upgrade/lead-ai-labs-hf-upgrade

# Stage all newly generated assets
git add .

# Commit changes
git commit -m "Build professional Lead.AI Labs Hugging Face upgrade"

# Push to GitHub main branch
git push origin main
```
