# Lead.AI Labs — Hugging Face Upgrade Launch Checklist

This checklist tracks quality assurance, platform sync, and deployment verification for the **Lead.AI Labs** Hugging Face upgrade launch.

---

## 📋 Quality Assurance & Verification Checklist

- [ ] **1. GitHub Control Center Completed**
  - All 18 repository files created and populated without placeholders.
  - Python scripts (`app.py`, dataset generators) syntax-checked and verified.
  - Zero hard-coded credentials or API keys checked into code.

- [ ] **2. Hugging Face Organization Card Updated**
  - Content from `org-card/README.md` copy-pasted into [Hugging Face Lead.AI Labs Org Profile](https://huggingface.co/lead-ai-labs).
  - Web links to `www.lead-ai.us` and GitHub verified.

- [ ] **3. Model Card Uploaded**
  - `models/fraud-detection-xai/README.md` deployed to `lead-ai-labs/fraud-detection-xai`.
  - Responsible AI disclaimer verified on model landing page.

- [ ] **4. Dataset Cards Uploaded**
  - `datasets/fraud-detection-Table-data/README.md` pushed to `lead-ai-labs/fraud-detection-Table-data`.
  - `datasets/fraud-detection-sample-data/README.md` pushed to `lead-ai-labs/fraud-detection-sample-data`.

- [ ] **5. Synthetic Dataset CSV Files Uploaded**
  - `train.csv` (105 rows) uploaded to `lead-ai-labs/fraud-detection-Table-data`.
  - `sample_data.csv` (25 rows) uploaded to `lead-ai-labs/fraud-detection-sample-data`.

- [ ] **6. Hugging Face Dataset Viewer Verified**
  - Navigated to dataset pages on HF to ensure automatic tabular preview loads smoothly.

- [ ] **7. Space Repository Created & Configured**
  - Space `lead-ai-labs/lead-ai-fraud-shield-demo` provisioned with Gradio SDK.
  - `app.py`, `requirements.txt`, and `README.md` deployed.

- [ ] **8. Space Demo Running & Tested**
  - Tested example presets (Low Risk, High Fraud Risk).
  - Verified XAI feature contribution calculations render properly.

- [ ] **9. Hugging Face Collections Assembled**
  - Created 4 curated collections per `collections/collection-plan.md`.
  - Pinned "Lead.AI Fraud Shield" collection to Org profile.

- [ ] **10. Official Website Cross-Linked**
  - Added Hugging Face & GitHub portfolio badges to [www.lead-ai.us](https://www.lead-ai.us).

- [ ] **11. Founder LinkedIn Launch Post Published**
  - Posted announcement using template in `launch/LINKEDIN_POST.md`.

- [ ] **12. Lead.AI Contact CTA Tested**
  - Tested form submission / consultation booking on `www.lead-ai.us`.
