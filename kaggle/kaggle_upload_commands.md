# Lead.AI Labs — Kaggle Safe Upload & Sync Commands

This guide provides safe, tested command-line scripts to upload and synchronize datasets and notebooks to [Kaggle](https://www.kaggle.com/arungharami) using the official Kaggle CLI.

> ⚠️ **SECURITY MANDATE:** Never hard-code private credentials or store `kaggle.json` inside the repository. Always place your API token in `~/.kaggle/kaggle.json` or use environment variables (`KAGGLE_USERNAME`, `KAGGLE_KEY`).

---

## 🔑 1. Kaggle CLI Setup & Authentication

Run these commands in your Mac terminal session:

```bash
# 1. Install or update the Kaggle CLI package
pip install --upgrade kaggle

# 2. Credential Setup Instructions:
# - Log into Kaggle: https://www.kaggle.com
# - Navigate to: Account Settings -> API -> "Create New Token"
# - Download kaggle.json and move it to your home directory:
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json

# 3. Set strict read/write permissions on kaggle.json (Security Requirement)
chmod 600 ~/.kaggle/kaggle.json

# 4. Test authentication by listing Lead.AI datasets
kaggle datasets list -s "Lead.AI"
```

---

## 📊 2. Publish Datasets to Kaggle

Navigate to your repo root before running these commands:

```bash
cd /Users/arun/Documents/Lead-ai-labs-hf-upgrade/lead-ai-labs-hf-upgrade
```

### A. Publish Training Dataset (`arungharami/lead-ai-fraud-detection-table-data`)

```bash
# Initial creation of dataset 1
kaggle datasets create -p kaggle/fraud-detection-table-data

# Update dataset version (if dataset already exists on Kaggle)
kaggle datasets version -p kaggle/fraud-detection-table-data \
  -m "Update Lead.AI fraud detection table dataset"
```

### B. Publish Sample Dataset (`arungharami/lead-ai-fraud-detection-sample-data`)

```bash
# Initial creation of dataset 2
kaggle datasets create -p kaggle/fraud-detection-sample-data

# Update dataset version (if dataset already exists on Kaggle)
kaggle datasets version -p kaggle/fraud-detection-sample-data \
  -m "Update Lead.AI fraud detection sample dataset"
```

---

## 📓 3. Publish Interactive Demo Notebook to Kaggle

```bash
# Push notebook kernel to Kaggle
kaggle kernels push -p kaggle/notebooks
```

---

## 🛠️ 4. Troubleshooting Guide

* **Error: `Unauthorized` / `401`:** Verify `~/.kaggle/kaggle.json` exists and permissions are set (`chmod 600 ~/.kaggle/kaggle.json`).
* **Error: `Dataset already exists`:** Use `kaggle datasets version` instead of `kaggle datasets create`.
* **Error: `Invalid dataset-metadata.json`:** Ensure `id`, `licenses`, `title`, and `subtitle` keys are properly formatted JSON without missing trailing quotes.
* **Error: `Kernel metadata not found`:** Verify `kaggle/notebooks/notebook-metadata.json` points to `lead_ai_fraud_shield_kaggle_demo.ipynb`.
