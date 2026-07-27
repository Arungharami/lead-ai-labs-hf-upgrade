---
license: mit
task_categories:
- tabular-classification
language:
- en
tags:
- fraud-detection
- sample-data
- explainable-ai
- xai
- financial-ai
- risk-scoring
- lead-ai
pretty_name: Lead.AI Fraud Detection Sample Data
size_categories:
- n<1K
---

# Lead.AI Fraud Detection Sample Data

The **Lead.AI Fraud Detection Sample Data** dataset (`lead-ai-labs/fraud-detection-sample-data`) is a lightweight 25-row synthetic dataset designed for rapid API integration testing, demo validation, and sample tabular fraud detection experimentation.

---

## 📌 Dataset Summary

* **Dataset Name:** Lead.AI Fraud Detection Sample Data
* **Repository:** `lead-ai-labs/fraud-detection-sample-data`
* **Publisher:** [Lead.AI Labs](https://huggingface.co/lead-ai-labs)
* **License:** MIT License
* **Task Category:** Tabular Classification
* **Format:** CSV (`sample_data.csv`)
* **Size:** 25 synthetic transaction records

---

## 📊 Schema Reference

Contains the exact 11-column tabular schema as `lead-ai-labs/fraud-detection-Table-data`:
`transaction_id`, `amount`, `transaction_hour`, `merchant_risk_score`, `customer_age_days`, `device_trust_score`, `location_risk_score`, `velocity_24h`, `previous_chargebacks`, `payment_method_risk`, `is_fraud`.

---

## 🎯 Intended Use

* Rapid sanity testing of inference code and Gradio apps.
* Light API testing without downloading large CSV files.
* Educational demonstration of tabular feature structures.

---

## 🛡️ Synthetic Data Disclaimer

> **IMPORTANT DATASET NOTE:**
> This dataset is synthetic transaction-style data created for fraud detection experimentation, XAI demonstrations, and Lead.AI product prototyping. It does not contain real customer data, real card numbers, private banking data, or personally identifiable information.

---

## 🔗 Related Resources

* 📂 **Full Training Dataset:** [lead-ai-labs/fraud-detection-Table-data](https://huggingface.co/datasets/lead-ai-labs/fraud-detection-Table-data)
* 🤖 **Associated Model:** [lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai)
* 🖥️ **Live Space Demo:** [lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 🌐 **Official Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
