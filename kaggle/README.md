# Lead.AI Labs — Kaggle CLI Bridge Architecture

This directory houses the **Kaggle CLI Bridge** for **Lead.AI Labs** ([www.lead-ai.us](https://www.lead-ai.us)), enabling automated publishing, versioning, and management of public data science assets and interactive notebooks on Kaggle ([kaggle.com/arungharami](https://www.kaggle.com/arungharami)).

---

## 🏛️ Strategic Positioning & Ecosystem Role

> **Kaggle Positioning:** Kaggle serves as the public data-science showcase layer for Lead.AI Labs. While Hugging Face hosts AI model weights, dataset cards, and live Gradio Space demos, and GitHub hosts core engineering source code, Kaggle hosts notebook-style exploratory data analysis (EDA), benchmark kernel runs, and dataset discovery—with [www.lead-ai.us](https://www.lead-ai.us) acting as the final enterprise client conversion hub.

```
THE 4-PLATFORM PRODUCT ECOSYSTEM

  [ www.lead-ai.us ] ◄── Enterprise Client Conversion & Service Packages
         ▲
         │
  [ GitHub Control Center ] ◄── Engineering Proof & Architecture Source
         ▲
         │
  [ Hugging Face Hub ] ◄── Open Models, Datasets & Interactive Space Demos
         ▲
         │
  [ Kaggle Data Science Bridge ] ◄── Benchmark Kernels & Notebook EDA
```

---

## 🎯 What This Kaggle Bridge Controls

1. **`kaggle/fraud-detection-table-data/`**: Metadata, documentation, and `train.csv` for Kaggle dataset `arungharami/lead-ai-fraud-detection-table-data`.
2. **`kaggle/fraud-detection-sample-data/`**: Metadata, documentation, and `sample_data.csv` for Kaggle dataset `arungharami/lead-ai-fraud-detection-sample-data`.
3. **`kaggle/notebooks/`**: Executable Jupyter Notebook (`lead_ai_fraud_shield_kaggle_demo.ipynb`) and metadata (`notebook-metadata.json`) for Kaggle kernel `arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo`.
4. **`kaggle/kaggle_upload_commands.md`**: CLI sync scripts for automated publishing via the official `kaggle` Python package.

---

## 🔒 Security & Credential Guidelines

> ⚠️ **CRITICAL SECURITY MANDATE:**
> Never commit `kaggle.json` or API keys to Git.
> All local credentials must reside exclusively at `~/.kaggle/kaggle.json` with restricted permissions (`chmod 600 ~/.kaggle/kaggle.json`) or be supplied via environment variables (`KAGGLE_USERNAME`, `KAGGLE_KEY`).
> The repository `.gitignore` explicitly blocks `kaggle.json`.

---

## 🔗 Cross-Platform Asset Mapping

* **Kaggle Profile:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami)
* **Kaggle Dataset 1:** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data)
* **Kaggle Dataset 2:** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-sample-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-sample-data)
* **Kaggle Demo Notebook:** [kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)
* **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us)
