# Lead.AI Labs Hugging Face & Kaggle Upgrade Control Center

[![Lead.AI Website](https://img.shields.io/badge/Website-lead--ai.us-00D2FF?style=for-the-badge&logo=google-chrome&logoColor=white)](https://www.lead-ai.us)
[![Hugging Face Org](https://img.shields.io/badge/Hugging%20Face-lead--ai--labs-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/lead-ai-labs)
[![Kaggle Profile](https://img.shields.io/badge/Kaggle-arungharami-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/arungharami)
[![GitHub Repo](https://img.shields.io/badge/GitHub-lead--ai--labs--hf--upgrade-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

This repository manages the professional Hugging Face and Kaggle upgrades for Lead.AI Labs, including organization card content, model cards, dataset cards, Space demo files, Kaggle CLI dataset/notebook bridge packages, upload commands, website link mapping, and launch materials.

---

## 🏢 Business Identity & Multi-Platform Links

* **Company Name:** Lead.AI Labs
* **Tagline:** Trustworthy AI, fraud detection, predictive analytics, and automation systems for real business workflows.
* **Founder:** Arun Kumar Gharami (AI Engineer & Applied Researcher)
* **Main Business Identity:** Explainable AI Systems for Business Automation
* **Official Website:** [www.lead-ai.us](https://www.lead-ai.us)
* **Hugging Face Organization:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs)
* **Kaggle Profile:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami)
* **GitHub Repository:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)

---

## 🎯 What This Repo Controls

This repository serves as the centralized **Upgrade Control Center** to maintain, package, and sync all public AI portfolio assets for Lead.AI Labs across Hugging Face and Kaggle:

1. **Organization Profile Card (`org-card/`):** Complete README markup for the Lead.AI Labs organization page.
2. **Explainable AI Model Cards (`models/`):** Detailed card, schema, and XAI documentation for `lead-ai-labs/fraud-detection-xai`.
3. **Structured Hugging Face Datasets (`datasets/`):** Clean tabular synthetic datasets and Hugging Face Dataset Viewer metadata (`fraud-detection-Table-data` & `fraud-detection-sample-data`).
4. **Interactive Hugging Face Space (`spaces/`):** Source code (`app.py`, `requirements.txt`, `README.md`) for the Gradio-powered `lead-ai-fraud-shield-demo`.
5. **Kaggle Data Science CLI Bridge (`kaggle/`):** Dataset metadata, Kaggle dataset packages, and executable Jupyter Notebook (`lead_ai_fraud_shield_kaggle_demo.ipynb`).
6. **Collection Architecture (`collections/`):** Blueprint for structuring 4 specialized Hugging Face collections.
7. **Website & Funnel Mapping (`website-link-map/`):** Navigation and cross-referencing strategy between `www.lead-ai.us`, GitHub, Hugging Face, and Kaggle.
8. **Automated Deployment Scripts (`upload_commands.md` & `kaggle/kaggle_upload_commands.md`):** Safe, credential-free CLI commands for Hugging Face and Kaggle.
9. **Product Launch Suite (`launch/`):** Launch checklist, LinkedIn announcement, and client pitch deck with service tier pricing.

---

## 📊 Kaggle & Hugging Face Platform Ecosystem Role

```text
[ www.lead-ai.us ] ◄── Enterprise Client Conversion & Service Packages
       ▲
       │
[ GitHub Control Center ] ◄── Open Source Engineering Proof
       ▲
       │
[ Hugging Face Hub ] ◄── Open Models, Datasets & Live Gradio Demos
       ▲
       │
[ Kaggle Data Science Bridge ] ◄── Benchmark Kernels & Notebook EDA Showcase
```

---

## 📂 Repository File Structure

```text
lead-ai-labs-hf-upgrade/
├── README.md                           # Main Control Dashboard (This file)
├── BRAND_GUIDE.md                      # Official Brand Identity & Tone Guidelines
├── PLATFORM_STRATEGY.md                # Multi-channel Business Funnel Strategy
├── FINAL_SUMMARY.md                    # Upgrade Audit & Executive Summary
├── upload_commands.md                  # Safe Hugging Face CLI Sync Scripts
├── org-card/
│   └── README.md                       # Content for HF Org Profile
├── models/
│   └── fraud-detection-xai/
│       └── README.md                   # Model Card for lead-ai-labs/fraud-detection-xai
├── datasets/
│   ├── fraud-detection-Table-data/
│   │   ├── README.md                   # Dataset Card with HF Viewer YAML
│   │   └── train.csv                   # 105-row synthetic tabular fraud dataset
│   └── fraud-detection-sample-data/
│       ├── README.md                   # Sample Dataset Card with HF Viewer YAML
│       └── sample_data.csv             # 25-row sample dataset
├── spaces/
│   └── lead-ai-fraud-shield-demo/
│       ├── README.md                   # HF Space Card
│       ├── app.py                      # Interactive Gradio XAI Demo App
│       └── requirements.txt            # Python Dependencies
├── kaggle/                             # NEW Kaggle CLI Bridge
│   ├── README.md                       # Kaggle Architecture Overview
│   ├── kaggle_upload_commands.md       # Kaggle CLI Publishing Scripts
│   ├── fraud-detection-table-data/     # Kaggle Dataset Package 1
│   │   ├── dataset-metadata.json
│   │   ├── README.md
│   │   └── train.csv
│   ├── fraud-detection-sample-data/    # Kaggle Dataset Package 2
│   │   ├── dataset-metadata.json
│   │   ├── README.md
│   │   └── sample_data.csv
│   └── notebooks/                      # Kaggle Kernel Package
│       ├── dataset-metadata.json / notebook-metadata.json
│       └── lead_ai_fraud_shield_kaggle_demo.ipynb
├── collections/
│   └── collection-plan.md              # 4 Curated Portfolio Collections
├── website-link-map/
│   └── lead-ai-platform-links.md       # Complete Cross-Platform URL System
├── launch/
│   ├── LAUNCH_CHECKLIST.md             # Pre-launch Quality Assurance Steps
│   ├── LINKEDIN_POST.md                # Founder Announcement Copy
│   └── CLIENT_PITCH.md                 # Client Outreach & Service Packages
└── .gitignore                          # Git & Credential Exclusions (kaggle.json blocked)
```

---

## 🚀 Quick Publishing Workflows

### 1. Hugging Face Deployment
```bash
export HF_TOKEN="your_huggingface_write_token_here"
huggingface-cli login --token $HF_TOKEN
# Refer to upload_commands.md for full repo sync scripts
```

### 2. Kaggle Deployment
```bash
# Setup ~/.kaggle/kaggle.json with chmod 600
kaggle datasets create -p kaggle/fraud-detection-table-data
kaggle datasets create -p kaggle/fraud-detection-sample-data
kaggle kernels push -p kaggle/notebooks
# Refer to kaggle/kaggle_upload_commands.md for detailed versioning commands
```

---

> **Safety Notice:** All datasets contained in this repository are 100% synthetic transaction data generated strictly for demonstration, evaluation, and research purposes. No real financial credentials, private card data, or PII are stored or processed.
