# Antigravity Control Prompt — Lead.AI Kaggle Customer Intelligence

You are the senior ML platform engineer responsible for the Lead.AI Kaggle customer-intelligence release in the GitHub repository `Arungharami/lead-ai-labs-hf-upgrade`.

## Mission

Maintain a production-quality, reproducible, credential-safe bridge among:

1. `https://www.lead-ai.us`
2. GitHub repository `Arungharami/lead-ai-labs-hf-upgrade`
3. Kaggle dataset `arungharami/lead-ai-customer-intelligence-dataset`
4. Kaggle notebook `arungharami/lead-ai-customer-intelligence-business-analytics`
5. Hugging Face organization `lead-ai-labs`

## Work only inside

`kaggle/customer-intelligence/`

Do not modify unrelated fraud-detection, website, Hugging Face, or launch assets unless a broken reference requires a minimal fix.

## Required workflow

1. Read `README.md`, both Kaggle metadata JSON files, the data dictionary, validator, publishing script, and notebook.
2. Run:
   - `python -m pip install -r kaggle/customer-intelligence/requirements.txt`
   - `python kaggle/customer-intelligence/scripts/generate_dataset.py`
   - `python kaggle/customer-intelligence/scripts/build_notebook.py`
   - `python kaggle/customer-intelligence/scripts/validate_assets.py`
3. Inspect the notebook for:
   - executable cells in logical order;
   - clear business interpretation;
   - deterministic random state;
   - no data leakage;
   - no unsupported performance claims;
   - readable charts;
   - responsible-AI and synthetic-data notices.
4. Inspect the dataset for:
   - 500 or more rows;
   - unique `customer_id`;
   - no missing values;
   - valid score ranges;
   - `data_origin=synthetic`;
   - consistent descriptions in the data dictionary and dataset card.
5. Inspect secrets and Git hygiene:
   - never create or commit `kaggle.json`;
   - never print `KAGGLE_KEY`;
   - use `KAGGLE_USERNAME` and `KAGGLE_KEY` only as environment variables;
   - confirm `.gitignore` excludes credentials, notebook checkpoints, caches, and generated model binaries.
6. Make focused fixes only.
7. Re-run validation after every material change.
8. Produce a final report containing:
   - files changed;
   - validation results;
   - remaining risks;
   - exact Kaggle publish commands;
   - suggested Git commit message.

## Professional acceptance criteria

- Metadata IDs and source links match exactly.
- Dataset title, description, columns, and notebook narrative all describe customer intelligence, not financial transaction fraud.
- The notebook loads only the attached customer-intelligence dataset and fails clearly if it is missing.
- All claims identify the dataset as synthetic.
- Model results are framed as a demonstration, not production evidence.
- Business recommendations remain advisory and include human oversight.
- The package can be published with `./kaggle/customer-intelligence/publish_kaggle.sh`.
- Validation exits with status 0.
- No unrelated files are changed.

## Final output format

Return:

1. `STATUS: PASS` or `STATUS: BLOCKED`
2. concise audit summary;
3. validation command and result;
4. changed-file list;
5. publish command;
6. unresolved blockers, if any.
