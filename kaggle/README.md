# Lead.AI Labs — Kaggle CLI Bridge Architecture

[![Website](https://img.shields.io/badge/Website-lead--ai.us-00D2FF?style=for-the-badge&logo=google-chrome&logoColor=white)](https://www.lead-ai.us)
[![GitHub](https://img.shields.io/badge/GitHub-lead--ai--labs--hf--upgrade-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-lead--ai--labs-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/lead-ai-labs)
[![Kaggle Profile](https://img.shields.io/badge/Kaggle-arungharami-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/arungharami)

This directory houses the **Kaggle CLI Bridge** for **Lead.AI Labs** ([www.lead-ai.us](https://www.lead-ai.us)), enabling automated publishing, versioning, and management of public data science assets and interactive notebooks on Kaggle ([kaggle.com/arungharami](https://www.kaggle.com/arungharami)).

---

## 🌉 The 4-Pillar Multi-Platform Ecosystem Bridge

```text
                        [ www.lead-ai.us ]
        (Official Business Website & Enterprise Conversion Hub)
                                ▲
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
 [ GitHub Control Center ] ◄► [ Hugging Face ] ◄► [ Kaggle Data Science ]
  Engineering Proof & Code    Models, Datasets &   Benchmark Kernels & 
  (Arungharami/lead-ai-       Interactive Space    Interactive EDA Notebooks
     labs-hf-upgrade)         Demos (lead-ai-labs)    (arungharami)
```

* 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us) — Enterprise AI solutions, custom risk modeling & consultation
* 💻 **GitHub Engineering Repo:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade) — Central upgrade control center, source code & CLI sync scripts
* 🤖 **Hugging Face Hub:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs) — Open-weight XAI models, tabular datasets & live Gradio web demos
* 📊 **Kaggle Data Science Hub:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami) — Benchmark kernels, Kaggle datasets & interactive exploratory notebook analysis

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

## 🔗 Cross-Platform Asset Mapping Directory

* 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us)
* 💻 **GitHub Engineering Repo:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
* 🤖 **Hugging Face Organization:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs)
* 🤖 **Hugging Face XAI Model:** [huggingface.co/lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai)
* 🖥️ **Hugging Face Live Gradio Demo:** [huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 📊 **Kaggle Profile:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami)
* 📊 **Kaggle Dataset 1 (Table Data):** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data)
* 📊 **Kaggle Dataset 2 (Sample Data):** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-sample-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-sample-data)
* 📓 **Kaggle Demo Notebook:** [kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)
