# Lead.AI Kaggle Customer Intelligence

Professional Kaggle dataset and notebook package for the Lead.AI customer-intelligence portfolio.

## Public targets

- Dataset: `arungharami/lead-ai-customer-intelligence-dataset`
- Notebook: `arungharami/lead-ai-customer-intelligence-business-analytics`
- Business website: [lead-ai.us](https://www.lead-ai.us)
- Engineering control center: [Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)

## Repository layout

```text
customer-intelligence/
├── README.md
├── requirements.txt
├── publish_kaggle.sh
├── dataset/
│   ├── README.md
│   ├── dataset-metadata.json
│   ├── data_dictionary.csv
│   └── lead_ai_customer_intelligence.csv
├── notebook/
│   ├── notebook-metadata.json
│   └── lead_ai_customer_intelligence_lab.ipynb
├── scripts/
│   ├── generate_dataset.py
│   ├── build_notebook.py
│   └── validate_assets.py
└── docs/
    └── ANTIGRAVITY_CONTROL_PROMPT.md
```

## Local validation

```bash
python -m pip install -r requirements.txt
python scripts/generate_dataset.py
python scripts/build_notebook.py
python scripts/validate_assets.py
```

## Kaggle publishing

Never commit `kaggle.json`. Use environment variables or the standard protected Kaggle configuration file.

```bash
export KAGGLE_USERNAME="arungharami"
export KAGGLE_KEY="your-secret-key"
chmod +x publish_kaggle.sh
./publish_kaggle.sh
```

The script validates the package, versions the existing dataset, and pushes the notebook.

## Quality standards

- deterministic synthetic data generated from source;
- explicit data dictionary;
- schema and range validation;
- unique identifiers;
- no missing values;
- reproducible notebook;
- interpretable model;
- responsible-AI limitations;
- cross-platform Lead.AI links;
- no credentials or personal data in Git.

## Release policy

Use semantic tags in GitHub:

- `kaggle-customer-intelligence-v1.0.0` — first professional release;
- patch versions for documentation or validation fixes;
- minor versions for new features or columns;
- major versions for schema-breaking changes.
