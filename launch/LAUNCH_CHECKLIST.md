# Lead.AI Labs — Hugging Face & Kaggle Launch Checklist

This checklist tracks quality assurance, multi-platform sync, and deployment verification for **Lead.AI Labs** ([www.lead-ai.us](https://www.lead-ai.us)), managed via the [GitHub Control Center](https://github.com/Arungharami/lead-ai-labs-hf-upgrade).

---

## 🌉 The 4-Pillar Multi-Platform Ecosystem Bridge

* 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us) — Enterprise AI solutions & consultation
* 💻 **GitHub Engineering Repo:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade) — Upgrade control center & code
* 🤖 **Hugging Face Hub:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs) — Models, datasets & Gradio space demo
* 📊 **Kaggle Data Science Hub:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami) — Benchmark datasets & notebook showcase

---

## 📋 Quality Assurance & Verification Checklist

- [ ] **1. GitHub Control Center Completed**
  - All repository files created and populated without placeholders.
  - Python scripts (`app.py`, dataset generators, notebook) syntax-checked and verified.
  - Zero hard-coded credentials or API keys checked into code.
  - `.gitignore` verified to block `kaggle.json`.

- [ ] **2. Hugging Face Organization Card Updated**
  - Content from `org-card/README.md` copy-pasted into [Hugging Face Lead.AI Labs Org Profile](https://huggingface.co/lead-ai-labs).
  - Web links to `www.lead-ai.us`, GitHub, and Kaggle verified.

- [ ] **3. Model & Dataset Cards Uploaded (Hugging Face)**
  - `models/fraud-detection-xai/README.md` deployed to `lead-ai-labs/fraud-detection-xai`.
  - Dataset cards & synthetic CSV files (`train.csv`, `sample_data.csv`) uploaded.
  - Dataset Viewer verified on Hugging Face.

- [ ] **4. Space Demo Created & Running (Hugging Face)**
  - Space `lead-ai-labs/lead-ai-fraud-shield-demo` provisioned and verified.

- [ ] **5. Kaggle Datasets Published**
  - `kaggle datasets create -p kaggle/fraud-detection-table-data` executed.
  - `kaggle datasets create -p kaggle/fraud-detection-sample-data` executed.
  - Verified datasets visible on [kaggle.com/arungharami](https://www.kaggle.com/arungharami).

- [ ] **6. Kaggle Notebook Kernel Published**
  - `kaggle kernels push -p kaggle/notebooks` executed.
  - Verified kernel runs and visualizes feature importances on Kaggle.

- [ ] **7. Hugging Face Collections Assembled**
  - Created 4 curated collections per `collections/collection-plan.md`.

- [ ] **8. Official Website Cross-Linked**
  - Added Hugging Face, GitHub, and Kaggle portfolio links to [www.lead-ai.us](https://www.lead-ai.us).

- [ ] **9. Founder LinkedIn Launch Post Published**
  - Posted announcement using template in `launch/LINKEDIN_POST.md` (including Kaggle links).

- [ ] **10. 4-Pillar Bridge Verification**
  - Verified bidirectional links across `www.lead-ai.us` ↔ GitHub ↔ Hugging Face ↔ Kaggle.

