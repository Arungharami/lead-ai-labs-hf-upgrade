---
title: Lead.AI Fraud Shield Demo
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.25.0
app_file: app.py
pinned: true
license: mit
short_description: Real-time explainable fraud detection & risk scoring AI
---

# Lead.AI Fraud Shield Demo

The **Lead.AI Fraud Shield Demo** is an interactive Explainable AI (XAI) risk-scoring portal engineered by **Lead.AI Labs** ([www.lead-ai.us](https://www.lead-ai.us)).

---

## 🎯 What This Demo Does

This application provides real-time fraud probability evaluation and explainable feature impact breakdowns for financial transactions. It demonstrates how machine learning models can assist risk analysts, fintech platforms, and e-commerce merchants by producing transparent, audit-ready risk scores instead of opaque predictions.

---

## 📥 How to Input Transaction Parameters

Users can adjust 9 core transaction variables:
1. **Transaction Amount ($):** Total value of purchase.
2. **Transaction Hour:** Time of day (0 to 23).
3. **Merchant Risk Score:** Industry classification risk index (0.0 to 1.0).
4. **Customer Account Age (Days):** Account history duration.
5. **Device Trust Score:** Hardware fingerprint score (0.0 = Untrusted, 1.0 = Verified).
6. **Location Risk Score:** Anomaly score for geo-location/VPN (0.0 to 1.0).
7. **Velocity (24h):** Transaction attempts in past 24 hours.
8. **Previous Chargebacks:** Count of past chargeback incidents.
9. **Payment Method Risk:** Risk score of the payment card/method used.

---

## 📤 Output Received

* **Risk Score (%):** Calculated probability of fraud ($0\% - 100\%$).
* **Risk Level:** `LOW RISK` (<30%), `MODERATE RISK` (30%–70%), `HIGH RISK` (>70%).
* **Prediction Status:** `Legitimate Transaction` or `Flagged for Fraud Risk`.
* **XAI Explanation:** Detailed feature attribution text identifying positive and negative risk factors.
* **Business Recommendation:** Actionable next step (e.g., *Auto-Approve*, *Step-Up 2FA*, *Manual Risk Review*, *Decline Order*).

---

## 🛡️ Responsible AI Disclaimer

> **NOTICE:** This demo application uses a weighted heuristic / synthetic benchmark model designed for portfolio presentation, research, education, and prototyping. It is not intended for standalone automated transaction blocking in live banking environments without domain-specific calibration and human analyst review. No real customer credit card or private banking data is stored or processed.

---

## 🌉 The 4-Pillar Multi-Platform Ecosystem Bridge

* 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us) — Enterprise AI solutions, custom risk modeling & consultation
* 💻 **GitHub Engineering Repo:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade) — Central upgrade control center & Gradio app code
* 🤖 **Hugging Face Space Demo:** [lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo) — Live interactive web application
* 📊 **Kaggle Profile & Datasets:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami) — Benchmark datasets & Kaggle kernel showcase
* 📓 **Kaggle Demo Kernel:** [kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo) — Executable Kaggle Jupyter demo

---

## 🔗 Connected Platform Links

* 🌐 **Official Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
* 💻 **GitHub Control Center:** [https://github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
* 🤖 **Hugging Face Model:** [lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai)
* 📊 **Hugging Face Dataset:** [lead-ai-labs/fraud-detection-Table-data](https://huggingface.co/datasets/lead-ai-labs/fraud-detection-Table-data)
* 📓 **Kaggle Benchmark Notebook:** [kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)
* 📊 **Kaggle Dataset 1:** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data)
