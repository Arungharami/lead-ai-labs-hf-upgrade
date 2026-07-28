# Lead.AI Customer Intelligence Dataset

A reproducible, synthetic customer-intelligence benchmark for small-business analytics, lead prioritization, churn-risk exploration, and workflow-automation research.

## Purpose

This dataset supports the Lead.AI ecosystem at [lead-ai.us](https://www.lead-ai.us) by providing a safe demonstration asset for:

- lead-quality scoring;
- customer segmentation;
- churn-risk analysis;
- automation-readiness assessment;
- next-best-action prototyping;
- dashboard and machine-learning tutorials.

## Files

| File | Purpose |
|---|---|
| `lead_ai_customer_intelligence.csv` | 500 synthetic business/customer records generated before validation/publishing |
| `data_dictionary.csv` | Column names, data types, and business definitions |
| `dataset-metadata.json` | Kaggle publishing metadata |

## Data Quality Contract

- **Rows:** 500
- **Columns:** 24
- **Missing values:** none by design
- **Duplicate customer IDs:** none
- **Currency fields:** U.S. dollars
- **Sensitive data:** none
- **Personal data:** none
- **Reproducibility seed:** 42

## Responsible Use

All records are synthetic. The dataset is designed for education, prototyping, portfolio demonstrations, and early-stage research. It must not be presented as real customer evidence, used to make consequential decisions about individuals, or treated as production-ready without domain validation, fairness testing, security review, and human oversight.

## Citation

```bibtex
@dataset{gharami_2026_lead_ai_customer_intelligence,
  author    = {Arun Kumar Gharami},
  title     = {Lead.AI Customer Intelligence Dataset},
  year      = {2026},
  publisher = {Kaggle},
  url       = {https://www.kaggle.com/datasets/arungharami/lead-ai-customer-intelligence-dataset}
}
```

## Ecosystem

- Website: [lead-ai.us](https://www.lead-ai.us)
- GitHub control center: [Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
- Hugging Face: [lead-ai-labs](https://huggingface.co/lead-ai-labs)
- Kaggle: [arungharami](https://www.kaggle.com/arungharami)

## Reproducible generation

Run `python ../scripts/generate_dataset.py` from this directory’s parent package. The generated CSV is intentionally excluded from Git and recreated deterministically before CI validation and Kaggle publishing.
