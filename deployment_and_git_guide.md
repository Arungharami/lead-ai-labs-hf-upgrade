# Lead.AI Labs — Deployment & Multi-Platform Publishing Command Guide

This comprehensive guide outlines the operational steps to publish, sync, deploy, and maintain all **Lead.AI Labs** open-science assets and web components across **[www.lead-ai.us](https://www.lead-ai.us)**, **GitHub**, **Hugging Face**, and **Kaggle**.

---

## 📑 A. Files Created & Updated Directory

### 1. Web & SEO Suite
- `website-component/LeadAIFraudShieldSection.jsx`: Production React + Tailwind CSS enterprise product section with 5 pricing tiers.
- `website-component/SEO_METADATA.md`: Meta tags, OpenGraph tags, JSON-LD Schema markup, and LinkedIn launch copy.

### 2. GitHub Documentation Suite
- `github/lead-ai-fraud-shield-README.md`: Master production README for `https://github.com/Arungharami/lead-ai-fraud-shield` with FastAPI snippet, architecture diagram, and 11 GitHub topics.
- `github/lead-ai-hf-portfolio-README.md`: Hub README for `https://github.com/Arungharami/lead-ai-hf-portfolio`.

### 3. Hugging Face Asset Suite
- `models/fraud-detection-xai/README.md`: Flagship model card with commercial CTA (`Visit: https://www.lead-ai.us`).
- `models/lead-ai-fraud-detection-model/README.md`: Model card for `arun-gharami/lead-ai-fraud-detection-model`.
- `models/lead-ai-customer-predictor/README.md`: Model card for `arun-gharami/lead-ai-customer-predictor` (CLV & Churn).
- `models/lead-ai-review-sentinel/README.md`: Model card for `arun-gharami/lead-ai-review-sentinel` (NLP Sentiment).
- `datasets/fraud-detection-Table-data/README.md`: Dataset card v2 (`arun-gharami/lead-ai-fraud-detection-dataset-v2`).
- `datasets/lead-ai-fraud-detection-dataset/README.md`: Dataset card v1 (`arun-gharami/lead-ai-fraud-detection-dataset`).
- `datasets/fraud-detection-sample-data/README.md`: Lightweight sample dataset card.
- `spaces/lead-ai-fraud-shield-demo/README.md` & `app.py`: Live Gradio web portal and card.
- `spaces/fraud-detection-xai-demo/README.md`: Space card for `arun-gharami/fraud-detection-xai-demo`.

### 4. Kaggle Bridge & Control Dashboard
- `kaggle/README.md`: Kaggle master architecture README with standard 4-pillar badges.
- `kaggle/fraud-detection-table-data/README.md`: Kaggle dataset 1 card.
- `kaggle/fraud-detection-sample-data/README.md`: Kaggle dataset 2 card.
- `kaggle/notebooks/lead_ai_fraud_shield_kaggle_demo.ipynb`: Kaggle Jupyter demo notebook.
- `README.md`, `PLATFORM_STRATEGY.md`, `FINAL_SUMMARY.md`, `website-link-map/lead-ai-platform-links.md`, `launch/LAUNCH_CHECKLIST.md`, `launch/CLIENT_PITCH.md`.

---

## 💻 B. Exact Git Commands Used

```bash
# 1. Check current Git status
git status

# 2. Stage all updated and newly created files
git add .

# 3. Commit with standard enterprise commit message
git commit -m "feat(brand): establish 4-pillar ecosystem bridge across website, GitHub, Hugging Face, and Kaggle"

# 4. Push to remote control center repository
git push origin main
```

---

## 🌐 C. Website Deployment Steps (`www.lead-ai.us`)

1. **Import Component:** Copy `website-component/LeadAIFraudShieldSection.jsx` into your React / Next.js app directory (e.g. `components/LeadAIFraudShieldSection.jsx`).
2. **Embed in Homepage:** Render `<LeadAIFraudShieldSection />` inside your main page layout (`pages/index.jsx` or `app/page.tsx`).
3. **Add Head Metadata:** Open `website-component/SEO_METADATA.md` and paste the `<head>` meta tags and JSON-LD `<script>` tag into your site index header.
4. **Deploy to Hosting:** Trigger build/deploy on Vercel, Netlify, Cloudflare Pages, or AWS:
   ```bash
   npm run build
   # Or push to main branch to trigger Vercel auto-deploy
   ```

---

## 🤖 D. Hugging Face Upload & Update Commands

```bash
# 1. Login to Hugging Face CLI (Use environment variable for write token)
export HF_TOKEN="your_huggingface_write_token_here"
huggingface-cli login --token $HF_TOKEN

# 2. Sync Model Cards
huggingface-cli upload arun-gharami/lead-ai-fraud-shield models/fraud-detection-xai/README.md README.md --repo-type model
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-model models/lead-ai-fraud-detection-model/README.md README.md --repo-type model
huggingface-cli upload arun-gharami/lead-ai-customer-predictor models/lead-ai-customer-predictor/README.md README.md --repo-type model
huggingface-cli upload arun-gharami/lead-ai-review-sentinel models/lead-ai-review-sentinel/README.md README.md --repo-type model

# 3. Sync Dataset Cards & Synthetic Data Files
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-dataset-v2 datasets/fraud-detection-Table-data/ . --repo-type dataset
huggingface-cli upload arun-gharami/lead-ai-fraud-detection-dataset datasets/lead-ai-fraud-detection-dataset/README.md README.md --repo-type dataset

# 4. Sync Space Demo Application
huggingface-cli upload lead-ai-labs/lead-ai-fraud-shield-demo spaces/lead-ai-fraud-shield-demo/ . --repo-type space
huggingface-cli upload arun-gharami/fraud-detection-xai-demo spaces/fraud-detection-xai-demo/README.md README.md --repo-type space
```

---

## 📊 E. Kaggle Upload & Update Commands

```bash
# 1. Verify credential permissions
chmod 600 ~/.kaggle/kaggle.json

# 2. Publish/Version Datasets
kaggle datasets create -p kaggle/fraud-detection-table-data
kaggle datasets create -p kaggle/fraud-detection-sample-data

# 3. Push Interactive Jupyter Notebook Kernel
kaggle kernels push -p kaggle/notebooks
```

---

## 🔗 F. Final Platform Link Map

```text
[ www.lead-ai.us ] ◄── Enterprise Client Conversion & Service Packages
       ▲
       │
[ GitHub Repositories ] ◄── Open Source FastAPI Code & Engineering Proof
       ▲
       │
[ Hugging Face Hub ] ◄── Open Models, Tabular Datasets & Live Gradio Demos
       ▲
       │
[ Kaggle Showcase ] ◄── Benchmark Datasets & Interactive EDA Kernels
```

* 🌐 **Official Website:** [https://www.lead-ai.us](https://www.lead-ai.us)
* 💻 **GitHub Main Repo:** [https://github.com/Arungharami/lead-ai-fraud-shield](https://github.com/Arungharami/lead-ai-fraud-shield)
* 💻 **GitHub Portfolio Repo:** [https://github.com/Arungharami/lead-ai-hf-portfolio](https://github.com/Arungharami/lead-ai-hf-portfolio)
* 🤖 **Hugging Face Profile:** [https://huggingface.co/arun-gharami](https://huggingface.co/arun-gharami)
* 🤖 **HF Flagship Model:** [https://huggingface.co/arun-gharami/lead-ai-fraud-shield](https://huggingface.co/arun-gharami/lead-ai-fraud-shield)
* 📊 **HF Dataset v2:** [https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2)
* 🖥️ **HF Live Space Demo:** [https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo](https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo)
* 📊 **Kaggle Profile:** [https://www.kaggle.com/arungharami](https://www.kaggle.com/arungharami)
* 📓 **Kaggle Demo Kernel:** [https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo](https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo)

---

## 🎯 G. Final Customer Funnel Summary

```text
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ DISCOVERY PHASE  │ ──► │ EVALUATION PHASE │ ──► │ CONSULTATION     │ ──► │ PAID INTEGRATION │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
  Kaggle Kernel, HF        Live Gradio Demo,        www.lead-ai.us Form,     Starter ($299+),
  Dataset v2, GitHub       SHAP Attributions,       60-Min Strategy Call     Professional ($999+),
  FastAPI Code             Model Card Schemas       with Arun Kumar Gharami  Business ($2,500+)
```

---

## 🏆 H. Final Business Positioning Statement

> **Lead.AI Labs is a professional AI automation and trustworthy machine learning company building explainable fraud detection, predictive analytics, customer intelligence, and AI workflow automation systems for businesses. Its flagship product, Lead.AI Fraud Shield, demonstrates production-style AI engineering across GitHub, Hugging Face, and www.lead-ai.us, creating a complete business funnel from public demo to paid integration services.**
