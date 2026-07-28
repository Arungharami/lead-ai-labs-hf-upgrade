from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split

from lead_ai_bench.data import (
    generate_synthetic_transactions,
    load_csv,
    load_huggingface_dataset,
    prepare_frame,
)
from lead_ai_bench.evaluation import evaluate_binary_classifier, select_threshold
from lead_ai_bench.model import save_model_bundle, train_candidate_models


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and evaluate the Lead.AI fraud model")
    parser.add_argument(
        "--source",
        choices=("synthetic", "csv", "huggingface"),
        default="synthetic",
    )
    parser.add_argument("--data-path", default="datasets/fraud-detection-Table-data/train.csv")
    parser.add_argument("--hf-repo", default="lead-ai-labs/fraud-detection-Table-data")
    parser.add_argument("--target-column", default=None)
    parser.add_argument("--synthetic-rows", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--minimum-recall", type=float, default=0.80)
    parser.add_argument("--output-dir", default="artifacts/fraud-detection-xai")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_metadata() -> dict[str, object]:
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "packages": {
            "joblib": joblib.__version__,
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit-learn": sklearn.__version__,
        },
        "serialization": "joblib/pickle-compatible; load only from a trusted revision",
    }


def write_checksum_manifest(output_dir: Path, filenames: list[str]) -> Path:
    manifest_path = output_dir / "SHA256SUMS.txt"
    lines = [f"{sha256_file(output_dir / name)}  {name}" for name in filenames]
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


def main() -> None:
    args = parse_args()
    if args.source == "synthetic":
        frame = generate_synthetic_transactions(args.synthetic_rows, args.seed)
        source_description = f"synthetic:{args.synthetic_rows}:seed={args.seed}"
    elif args.source == "csv":
        frame = load_csv(args.data_path)
        source_description = str(Path(args.data_path))
    else:
        frame = load_huggingface_dataset(args.hf_repo)
        source_description = f"hf://datasets/{args.hf_repo}"

    X, y, feature_names = prepare_frame(frame, args.target_column)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.40,
        stratify=y,
        random_state=args.seed,
    )
    X_validation, X_test, y_validation, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=args.seed,
    )

    training = train_candidate_models(X_train, y_train, seed=args.seed)
    validation_probability = training.estimator.predict_proba(X_validation)[:, 1]
    threshold = select_threshold(y_validation, validation_probability, args.minimum_recall)
    validation_metrics = evaluate_binary_classifier(
        training.estimator, X_validation, y_validation, threshold
    )
    test_metrics = evaluate_binary_classifier(training.estimator, X_test, y_test, threshold)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    runtime = runtime_metadata()
    metadata = {
        "generated_at": generated_at,
        "data_source": source_description,
        "seed": args.seed,
        "minimum_recall": args.minimum_recall,
        "feature_names": feature_names,
        "train_rows": int(len(X_train)),
        "validation_rows": int(len(X_validation)),
        "test_rows": int(len(X_test)),
        "runtime": runtime,
    }

    model_path = save_model_bundle(
        training,
        threshold,
        output_dir / "model.joblib",
        metadata,
    )

    report = {
        "metadata": metadata,
        "selected_model": training.selected_model,
        "candidate_scores": [score.__dict__ for score in training.candidate_scores],
        "validation": validation_metrics,
        "test": test_metrics,
        "limitations": [
            "Synthetic or public benchmark performance does not establish production performance.",
            "A financial institution must validate drift, fairness, calibration, and operating thresholds on its own labeled data.",
            "The model is a decision-support component, not an autonomous adverse-action system.",
        ],
    }

    metrics_path = output_dir / "metrics.json"
    schema_path = output_dir / "feature_schema.json"
    runtime_path = output_dir / "runtime.json"

    metrics_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    schema_path.write_text(
        json.dumps(
            {
                "features": feature_names,
                "target": args.target_column or "auto",
                "target_values": [0, 1],
                "identifier_columns_excluded": ["transaction_id", "id", "ID"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    runtime_path.write_text(json.dumps(runtime, indent=2), encoding="utf-8")

    write_checksum_manifest(
        output_dir,
        [model_path.name, metrics_path.name, schema_path.name, runtime_path.name],
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
