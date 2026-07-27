# Lead.AI Fraud Detection Table Data

The **Lead.AI Fraud Detection Table Data** dataset (`arungharami/lead-ai-fraud-detection-table-data`) is a structured tabular benchmark dataset engineered for tabular classification, Explainable AI (XAI) experiments, risk scoring model training, and financial fraud detection prototyping on Kaggle.

---

## 📌 Dataset Overview

* **Dataset Name:** Lead.AI Fraud Detection Table Data
* **Kaggle Slug:** `arungharami/lead-ai-fraud-detection-table-data`
* **Publisher:** [Lead.AI Labs](https://www.lead-ai.us)
* **Author:** Arun Kumar Gharami
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Format:** CSV (`train.csv`)
* **Size:** 105 realistic synthetic records

---

## 💡 Business Problem

Modern payment platforms and e-commerce merchants lose billions annually to fraudulent transactions and chargebacks. Traditional rule-based engines miss subtle fraud patterns, while standard "black-box" machine learning models provide high accuracy but lack transparency—making it impossible for risk officers to explain *why* a legitimate transaction was flagged or declined.

This dataset provides a controlled, noise-calibrated environment for building and evaluating transparent risk scoring models.

---

## 📊 Column Schema

| Column Name | Data Type | Range / Options | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id` | String | `TXN-1001`+ | Unique identifier for transaction record |
| `amount` | Float | `$10.50` – `$4850.00` | Transaction value in USD ($) |
| `transaction_hour` | Integer | `0` – `23` | Hour of transaction attempt (24h format) |
| `merchant_risk_score` | Float | `0.05` – `0.95` | Merchant category risk factor |
| `customer_age_days` | Integer | `1` – `1825` | Account history duration in days |
| `device_trust_score` | Float | `0.10` – `0.99` | Hardware/IP device fingerprint score |
| `location_risk_score` | Float | `0.05` – `0.95` | Geographic/Proxy/VPN risk index |
| `velocity_24h` | Integer | `1` – `28` | Transaction attempt count in past 24 hours |
| `previous_chargebacks` | Integer | `0` – `5` | Count of historical chargebacks recorded |
| `payment_method_risk` | Float | `0.10` – `0.90` | Risk factor of chosen payment instrument |
| `is_fraud` | Integer | `0` or `1` | **Target Label** (0 = Legitimate, 1 = Fraudulent) |

---

## 🔬 Machine Learning Tasks & Use Cases

1. **Tabular Classification:** Benchmark binary classifiers (XGBoost, LightGBM, Random Forest, Logistic Regression).
2. **Explainable AI (XAI) Attribution:** Compute SHAP values, LIME explanations, and feature importances.
3. **Risk Score Calibration:** Convert raw model probability outputs into risk tiers (Low, Moderate, High).

---

## 🌐 Connected Ecosystem Links

* 🤖 **Hugging Face Model:** [lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai)
* 📊 **Hugging Face Dataset:** [lead-ai-labs/fraud-detection-Table-data](https://huggingface.co/datasets/lead-ai-labs/fraud-detection-Table-data)
* 💻 **GitHub Control Center:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
* 🖥️ **Live Interactive Demo:** [lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 🌐 **Official Website:** [www.lead-ai.us](https://www.lead-ai.us)

---

## 🛡️ Responsible AI Disclaimer

> **IMPORTANT SYNTHETIC DATA NOTICE:**
> This dataset is synthetic transaction-style data created for fraud detection experimentation, XAI demonstrations, and Lead.AI product prototyping. It does not contain real customer data, real card numbers, private banking data, or personally identifiable information.

---

## 📄 Citation

```bibtex
@dataset{lead_ai_kaggle_table_data_2026,
  author = {Arun Kumar Gharami},
  title = {Lead.AI Fraud Detection Table Data},
  year = {2026},
  publisher = {Kaggle},
  howpublished = {\url{https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data}}
}
```
