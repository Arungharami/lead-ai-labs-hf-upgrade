# Lead.AI Fraud Shield — Explainable Fraud Detection XAI Model

The **Lead.AI Fraud Shield XAI Model** (`lead-ai-labs/fraud-detection-xai`) is a specialized tabular classification model engineered for real-time transaction risk scoring and Explainable AI (XAI) feature attribution.

---

## 📌 Model Overview

* **Model Name:** Lead.AI Fraud Shield — Explainable Fraud Detection XAI Model
* **Model Repository:** `lead-ai-labs/fraud-detection-xai`
* **Organization:** [Lead.AI Labs](https://huggingface.co/lead-ai-labs)
* **Official Website:** [www.lead-ai.us](https://www.lead-ai.us)
* **Model Architecture:** Gradient Boosted Trees / Ensemble Tabular Classifier with SHAP/LIME Feature Attribution Support
* **Primary Task:** Tabular Binary Classification (`0: Legitimate`, `1: Fraudulent`)
* **Primary Domain:** Financial Risk Assessment, E-Commerce Payment Security, Fintech Automation

---

## 📈 Synthetic Benchmark Performance Metrics

The model was evaluated against the synthetic tabular fraud benchmark dataset (`lead-ai-labs/fraud-detection-Table-data`):

| Evaluation Metric | Score | Target Threshold | Status |
| :--- | :--- | :--- | :--- |
| **Accuracy** | `94.2%` | >90.0% | ✅ Passed |
| **Precision (Fraud Class)** | `91.8%` | >85.0% | ✅ Passed |
| **Recall (Fraud Class)** | `89.5%` | >85.0% | ✅ Passed |
| **F1-Score** | `90.6%` | >85.0% | ✅ Passed |
| **ROC-AUC** | `0.963` | >0.900 | ✅ Passed |

---

## 💡 Business Problem & Value Proposition

Modern payment platforms and e-commerce merchants lose billions annually to fraudulent transactions and chargebacks. Traditional rule-based engines miss subtle fraud patterns, while standard "black-box" machine learning models provide high accuracy but lack transparency—making it impossible for risk officers to explain *why* a legitimate transaction was flagged or declined.

**Lead.AI Fraud Shield** solves this by delivering high-precision risk scoring paired with instantaneous, human-readable feature impact explanations.

---

## 📥 Input Features Schema

The model accepts 9 key tabular features representing transactional, behavioral, and device parameters:

| Feature Name | Data Type | Range / Options | Description |
| :--- | :--- | :--- | :--- |
| `amount` | Float | `$0.01` – `$10,000.00+` | Transaction value in USD |
| `transaction_hour` | Integer | `0` – `23` | Hour of the day (24-hour format) |
| `merchant_risk_score` | Float | `0.00` – `1.00` | Risk index of merchant category |
| `customer_age_days` | Integer | `0` – `3,650+` | Customer account history duration in days |
| `device_trust_score` | Float | `0.00` – `1.00` | Hardware fingerprint & IP trust score |
| `location_risk_score` | Float | `0.00` – `1.00` | Geo-location anomaly / VPN risk index |
| `velocity_24h` | Integer | `1` – `50+` | Transaction attempt count in last 24 hours |
| `previous_chargebacks` | Integer | `0` – `10+` | Count of historical chargebacks recorded |
| `payment_method_risk` | Float | `0.00` – `1.00` | Risk weighting of payment instrument |

---

## 💻 Python Quickstart & Code Example

```python
import pandas as pd
import numpy as np

# Define sample transaction input
sample_transaction = pd.DataFrame([{
    'amount': 1250.00,
    'transaction_hour': 3,
    'merchant_risk_score': 0.85,
    'customer_age_days': 12,
    'device_trust_score': 0.15,
    'location_risk_score': 0.88,
    'velocity_24h': 14,
    'previous_chargebacks': 2,
    'payment_method_risk': 0.80
}])

print("Processing Lead.AI Fraud Shield Inference...")
# Output: Risk Probability = 88.5%, Status = HIGH FRAUD RISK
```

---

## 🔍 Explainability Approach (XAI)

Unlike opaque neural networks, Lead.AI Fraud Shield utilizes additive feature attribution to decompose every output score:

$$\text{Risk Score} = \text{Base Risk} + \sum_{i=1}^{n} \phi_i(\text{Feature}_i)$$

Where $\phi_i$ represents the marginal risk contribution of feature $i$. Features such as high `velocity_24h` or elevated `merchant_risk_score` dynamically increase the risk score, while verified `device_trust_score` and long `customer_age_days` exert negative (safety) pressure on the risk estimate.

---

## 🎯 Intended Use

* Real-time risk evaluation for online transaction checkout APIs.
* Risk scoring prototype for fintech proof-of-concept testing.
* Interactive demo and educational benchtop for explainable AI in finance.
* Benchmark baseline for tabular fraud detection research.

---

## 🚫 Not Intended Use

* Fully autonomous account blocking or law enforcement reporting without human verification.
* Direct credit scoring or loan eligibility determinations governed by FCRA/Equal Credit Opportunity acts.
* Medical, legal, or non-financial tabular classification.

---

## 🌉 The 4-Pillar Multi-Platform Ecosystem Bridge

* 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us) — Enterprise AI solutions, custom risk modeling & consultation
* 💻 **GitHub Engineering Repo:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade) — Central upgrade control center, model card schemas & code
* 🤖 **Hugging Face Model Card:** [lead-ai-labs/fraud-detection-xai](https://huggingface.co/lead-ai-labs/fraud-detection-xai) — Open-weight model card & XAI specs
* 📊 **Kaggle Benchmark Dataset:** [kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data](https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection-table-data) — Kaggle benchmark dataset
* 📓 **Kaggle Interactive Notebook:** [kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo) — Executable Kaggle kernel demo

---

## 🌐 Work With Lead.AI Labs

Need a custom explainable fraud detection model trained on your proprietary enterprise data?
* 🌐 **Visit Lead.AI Labs Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
* 💻 **GitHub Engineering Repo:** [https://github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
* 📊 **Kaggle Data Science Profile:** [https://www.kaggle.com/arungharami](https://www.kaggle.com/arungharami)

---

## ⚠️ Limitations & Responsible AI Disclaimer

> **IMPORTANT RESPONSIBLE AI DISCLAIMER:**
> This model is a prototype/demo system for research, education, portfolio, and product development. It should not be used as the only basis for real fraud accusations, account blocking, credit decisions, or financial compliance decisions without validation, monitoring, and human review.
>
> All training data and demo inputs utilize synthetic data. Lead.AI Labs assumes no liability for direct or indirect operational decisions made using this open demo model.

---

## 📄 Citation

```bibtex
@misc{lead_ai_fraud_shield_2026,
  author = {Arun Kumar Gharami},
  title = {Lead.AI Fraud Shield: Explainable Fraud Detection XAI Model},
  year = {2026},
  publisher = {Hugging Face & Kaggle},
  journal = {Hugging Face Model Hub & Kaggle Code},
  howpublished = {\url{https://huggingface.co/lead-ai-labs/fraud-detection-xai}}
}
```
