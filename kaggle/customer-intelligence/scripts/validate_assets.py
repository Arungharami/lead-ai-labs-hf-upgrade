#!/usr/bin/env python3
"""Validate Lead.AI Kaggle dataset and notebook assets before publishing."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import nbformat
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
NOTEBOOK_DIR = ROOT / "notebook"


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_json(path: Path) -> dict:
    if not path.exists():
        fail(f"Missing required JSON file: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    dataset_meta = validate_json(DATASET_DIR / "dataset-metadata.json")
    notebook_meta = validate_json(NOTEBOOK_DIR / "notebook-metadata.json")

    if dataset_meta["id"] != "arungharami/lead-ai-customer-intelligence-dataset":
        fail("Unexpected Kaggle dataset id")
    if notebook_meta["dataset_sources"] != [dataset_meta["id"]]:
        fail("Notebook metadata must reference the dataset id")

    csv_path = DATASET_DIR / "lead_ai_customer_intelligence.csv"
    df = pd.read_csv(csv_path)
    if len(df) < 500:
        fail("Dataset must contain at least 500 rows")
    if df["customer_id"].duplicated().any():
        fail("customer_id contains duplicates")
    if df.isna().any().any():
        fail("Dataset contains missing values")
    if not df["data_origin"].eq("synthetic").all():
        fail("Every row must declare synthetic origin")

    notebook_path = NOTEBOOK_DIR / notebook_meta["code_file"]
    notebook = nbformat.read(notebook_path, as_version=4)
    if len(notebook.cells) < 10:
        fail("Notebook is missing expected analytical sections")

    print(
        f"PASS: {len(df)} rows, {len(df.columns)} columns, "
        f"{len(notebook.cells)} notebook cells."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
