#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python -m pip install -r requirements.txt
python scripts/generate_dataset.py
python scripts/build_notebook.py
python scripts/validate_assets.py

: "${KAGGLE_USERNAME:?Set KAGGLE_USERNAME}"
: "${KAGGLE_KEY:?Set KAGGLE_KEY}"

kaggle datasets version \
  -p dataset \
  -m "Professional Lead.AI customer-intelligence dataset refresh" \
  --dir-mode zip

kaggle kernels push -p notebook

echo "Kaggle dataset and notebook submitted successfully."
