# Lead.AI Fraud Shield — Explainable Fraud Detection & Risk Scoring System

[![Website](https://img.shields.io/badge/Website-lead--ai.us-00D2FF?style=for-the-badge&logo=google-chrome&logoColor=white)](https://www.lead-ai.us)
[![GitHub Repo](https://img.shields.io/badge/GitHub-lead--ai--fraud--shield-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Arungharami/lead-ai-fraud-shield)
[![Hugging Face Model](https://img.shields.io/badge/Hugging%20Face-lead--ai--fraud--shield-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/arun-gharami/lead-ai-fraud-shield)
[![Kaggle Notebook](https://img.shields.io/badge/Kaggle-Demo%20Notebook-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

**Lead.AI Fraud Shield** is an explainable fraud detection and risk-scoring AI system engineered for small businesses, fintech platforms, e-commerce stores, payment review teams, and AI automation clients. Built by **Lead.AI Labs** ([www.lead-ai.us](https://www.lead-ai.us)).

---

## 📌 Topics / Tags
`fraud-detection` · `explainable-ai` · `xai` · `shap` · `fastapi` · `machine-learning` · `fintech` · `ai-automation` · `predictive-analytics` · `lead-ai` · `trustworthy-ai`

---

## 💡 Business Problem & Product Overview

Modern payment gateways, e-commerce stores, and fintech platforms lose billions annually to fraudulent transactions and chargeback disputes. Traditional rule-based engines miss subtle velocity anomalies, while standard "black-box" machine learning models provide high accuracy but lack transparency—making it impossible for risk officers to explain *why* a legitimate transaction was flagged or declined.

**Lead.AI Fraud Shield** solves this by delivering high-precision gradient boosted tabular classification paired with **Explainable AI (SHAP / LIME)** feature attributions and a production-ready **FastAPI** web framework.

---

## 🎯 Who It Helps

* 💳 **Fintech & Payment Gateway Engineers:** Pre-screen transactions with real-time API risk scores before authorization.
* 🛍️ **E-Commerce Risk Analysts:** Reduce manual review queues by up to 70% with human-interpretable feature impact breakdowns.
* 🛡️ **Small Business Merchants:** Lower chargeback ratios and prevent customer friction caused by false positives.
* 🤖 **AI Automation Consultants:** Embed transparent ML risk models into enterprise microservice architectures.

---

## 🌟 Key Features

* ⚡ **Real-Time Risk Probability (0–100%):** Instant tabular classification using optimized gradient boosted decision trees.
* 🔬 **SHAP & LIME Feature Attribution:** Quantitative breakdown explaining positive (risk) and negative (safety) factors.
* 🚦 **Calibrated Risk Assessment Tiers:** `LOW RISK` (<30%), `MODERATE RISK` (30–70%), `HIGH RISK` (>70%).
* 🛑 **Automated Business Action Routing:** Auto-Approve, Challenge via 3DS 2.0 / OTP, or Route to Manual Review.
* 🔌 **Production FastAPI Endpoint:** High-throughput JSON REST API with Pydantic schema validation.
* 🖥️ **Interactive Gradio Portal:** Embedded web application for live testing and demonstration.

---

## 🏗️ System Architecture

```text
  [ Client Request / Payment Gateway API ]
                     │ (JSON Input Payload)
                     ▼
       ┌───────────────────────────┐
       │   FastAPI Web Microservice│
       └─────────────┬─────────────┘
                     │ (Validation via Pydantic)
                     ▼
       ┌───────────────────────────┐
       │ Lead.AI Fraud Shield ML   │ ◄── [ Tabular Benchmark Model ]
       └─────────────┬─────────────┘
                     │ (Probability & SHAP Attributions)
                     ▼
       ┌───────────────────────────┐
       │  SHAP XAI Feature Engine  │
       └─────────────┬─────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  [ Risk Score (%) ]   [ Feature Attribution Table ] ──► [ Business Recommendation ]
```

---

## 🔗 Live Demo & Connected Assets

* 🌐 **Official Business Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
* 🖥️ **Live Gradio Space Demo:** [https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 🤖 **Hugging Face Model Card:** [https://huggingface.co/arun-gharami/lead-ai-fraud-shield](https://huggingface.co/arun-gharami/lead-ai-fraud-shield)
* 📊 **Hugging Face Dataset v2:** [https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2)
* 📓 **Kaggle Benchmark Kernel:** [https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)

---

## ⚡ FastAPI Production Code Example

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Lead.AI Fraud Shield API", version="1.0.0")

class TransactionPayload(BaseModel):
    amount: float = Field(..., example=1250.00)
    transaction_hour: int = Field(..., ge=0, le=23, example=3)
    merchant_risk_score: float = Field(..., ge=0.0, le=1.0, example=0.85)
    customer_age_days: int = Field(..., ge=0, example=12)
    device_trust_score: float = Field(..., ge=0.0, le=1.0, example=0.15)
    location_risk_score: float = Field(..., ge=0.0, le=1.0, example=0.88)
    velocity_24h: int = Field(..., ge=1, example=14)
    previous_chargebacks: int = Field(..., ge=0, example=2)
    payment_method_risk: float = Field(..., ge=0.0, le=1.0, example=0.80)

@app.post("/api/v1/score-transaction")
def score_transaction(payload: TransactionPayload):
    # Simulated Lead.AI XAI Risk Engine
    risk_score = 88.5
    return {
        "status": "success",
        "risk_probability_pct": risk_score,
        "risk_tier": "HIGH RISK TIER (>70%)",
        "recommendation": "DECLINE & ROUTE TO MANUAL REVIEW QUEUE",
        "top_xai_factors": [
            {"factor": "24-Hour Velocity", "impact": "+25.0%", "type": "Risk Driver"},
            {"factor": "Transaction Amount", "impact": "+22.0%", "type": "Risk Driver"},
            {"factor": "Customer Account Age", "impact": "+18.0%", "type": "Risk Driver"}
        ]
    }
```

---

## 🛠️ Local Setup & Environment

```bash
# Clone the repository
git clone https://github.com/Arungharami/lead-ai-fraud-shield.git
cd lead-ai-fraud-shield

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI microservice
uvicorn app:app --reload --port 8000
```

---

## 🔒 Security, Privacy & Responsible AI Notes

> ⚠️ **IMPORTANT RESPONSIBLE AI & PRIVACY NOTICE:**
> All demonstration datasets, API endpoints, and model benchmarks in this repository utilize **100% synthetic data**. No real banking data, private credit card credentials, or personally identifiable information (PII) are stored, logged, or processed.
>
> Zero API keys, Hugging Face write tokens, Kaggle credentials, or database secrets are hard-coded into this codebase. All production environment configurations require strictly managed environment variables (`.env`).

---

## 🛍️ Enterprise Service Packages & Consultation CTA

| Tier | Price | Description | Primary Value |
| :--- | :--- | :--- | :--- |
| **Free Demo** | `$0.00` | Open HF demo, Kaggle notebook, and public dataset. | Self-guided testing |
| **Starter** | `$299+` | Custom risk evaluation report on up to 50k records. | Feature attribution audit |
| **Professional** | `$999+` | Custom XAI fraud model trained on client data + API specs. | Private dashboard & code |
| **Business** | `$2,500+` | End-to-end cloud production deployment + drift monitoring. | Automated cloud microservice |
| **Enterprise** | `Custom` | On-premise VPC setup, dedicated SLA, and fine-tuning. | Private VPC & SLA |

👉 **Want Lead.AI Fraud Shield customized for your company?**
Book a technical consultation with Lead.AI Labs: [https://www.lead-ai.us](https://www.lead-ai.us)

---

## 🏢 Founder & Lead.AI Labs Credibility

**Lead.AI Labs** is founded by **Arun Kumar Gharami**, an AI Engineer & Applied Researcher specializing in Computer Science, Artificial Intelligence, Machine Learning, QA validation, explainable AI, fraud detection, predictive analytics, and deployment-ready AI systems.

* 🌐 **Official Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
* 💻 **GitHub Profile:** [https://github.com/Arungharami](https://github.com/Arungharami)
* 🤖 **Hugging Face Hub:** [https://huggingface.co/arun-gharami](https://huggingface.co/arun-gharami)
* 📊 **Kaggle Profile:** [https://www.kaggle.com/arungharami](https://www.kaggle.com/arungharami)
