---
license: cc-by-4.0
task_categories:
- tabular-classification
language:
- en
tags:
- fraud-detection
- explainable-ai
- xai
- financial-ai
- risk-scoring
- trustworthy-ai
- tabular-classification
- lead-ai
pretty_name: Lead.AI Fraud Detection Table Data
size_categories:
- 1K<n<10K
---

# Lead.AI Fraud Detection Table Data

The **Lead.AI Fraud Detection Table Data** dataset (`lead-ai-labs/fraud-detection-Table-data`) is a structured tabular benchmark dataset engineered for tabular classification, Explainable AI (XAI) experiments, risk scoring model training, and financial fraud detection prototyping.

---

## 📌 Dataset Summary

* **Dataset Name:** Lead.AI Fraud Detection Table Data
* **Repository:** `lead-ai-labs/fraud-detection-Table-data`
* **Publisher:** [Lead.AI Labs](https://huggingface.co/lead-ai-labs)
* **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
* **Task Category:** Tabular Classification
* **Format:** CSV (`train.csv`)
* **Size:** 100+ realistic synthetic records

---

## 🎯 Dataset Purpose

This dataset provides a balanced, noise-injected tabular environment designed specifically to benchmark binary classification models and explainability frameworks (SHAP, LIME, Feature Importance). It reflects common transactional, behavioral, and device risk signals encountered in online payment processing and e-commerce checkout systems.

---

## 🔬 Data Source & Creation Method

* **Generation Strategy:** Algorithmic synthetic data generation using stochastic multivariate distributions calibrated against empirical financial fraud risk indicators.
* **Correlations Included:**
  * High transaction amount + low account age correlates positively with fraud risk.
  * High velocity in 24 hours + high location risk correlates strongly with fraud risk.
  * High device trust score + high customer account age correlates negatively with fraud risk.

---

## 📊 Column Schema

| Column Name | Data Type | Range / Options | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id` | String | `TXN-1001`+ | Unique identifier for the transaction record |
| `amount` | Float | `10.50` – `4850.00` | Transaction value in USD ($) |
| `transaction_hour` | Integer | `0` – `23` | Hour of transaction attempt (24h format) |
| `merchant_risk_score` | Float | `0.05` – `0.95` | Merchant category risk factor |
| `customer_age_days` | Integer | `1` – `1825` | Account history duration in days |
| `device_trust_score` | Float | `0.10` – `0.99` | Hardware/IP device fingerprint verification score |
| `location_risk_score` | Float | `0.05` – `0.95` | Geographic/Proxy/VPN risk weighting |
| `velocity_24h` | Integer | `1` – `28` | Number of transactions attempted in past 24 hours |
| `previous_chargebacks` | Integer | `0` – `5` | Count of historical chargebacks recorded |
| `payment_method_risk` | Float | `0.10` – `0.90` | Risk factor of chosen payment instrument |
| `is_fraud` | Integer | `0` or `1` | **Target Label** (0 = Legitimate, 1 = Fraudulent) |

---

## 🎯 Target Label

* `0`: **Legitimate Transaction** (Normal user activity, verified pattern).
* `1`: **Fraudulent Transaction** (High-risk anomaly, flagged for chargeback or fraud prevention).

---

## 📝 Example Rows

```csv
transaction_id,amount,transaction_hour,merchant_risk_score,customer_age_days,device_trust_score,location_risk_score,velocity_24h,previous_chargebacks,payment_method_risk,is_fraud
TXN-1001,45.20,14,0.15,450,0.92,0.10,2,0,0.15,0
TXN-1002,1250.00,3,0.85,12,0.15,0.88,14,2,0.80,1
TXN-1003,89.99,18,0.20,120,0.88,0.15,1,0,0.20,0
```

---

## Intended Use

* Training tabular classification algorithms (XGBoost, LightGBM, Random Forest, Logistic Regression).
* Evaluating Explainable AI (XAI) feature attribution accuracy.
* Prototyping risk-scoring web interfaces and API endpoints.

---

## Not Intended Use

* Direct production deployment for real-money financial decision-making without real-world model fine-tuning.
* Use as a representative sample of any specific bank's proprietary customer transaction history.

---

## 🛡️ Ethical Use & Responsible AI Notes

> **IMPORTANT DATASET NOTE:**
> This dataset is synthetic transaction-style data created for fraud detection experimentation, XAI demonstrations, and Lead.AI product prototyping. It does not contain real customer data, real card numbers, private banking data, or personally identifiable information.

---

## 🔗 Related Resources

* 🤖 **Associated Model:** [lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai)
* 🖥️ **Live Space Demo:** [lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 🌐 **Official Website:** [https://www.lead-ai.us](https://www.lead-ai.us)

---

## 📄 Citation

```bibtex
@dataset{lead_ai_table_data_2026,
  author = {Arun Kumar Gharami},
  title = {Lead.AI Fraud Detection Table Data},
  year = {2026},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/lead-ai-labs/fraud-detection-Table-data}}
}
```
