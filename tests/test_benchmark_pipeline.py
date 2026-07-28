from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

from lead_ai_bench.data import generate_synthetic_transactions, prepare_frame
from lead_ai_bench.evaluation import expected_calibration_error, evaluate_binary_classifier, select_threshold
from lead_ai_bench.model import load_model_bundle, save_model_bundle, train_candidate_models


def test_generator_is_reproducible_and_binary():
    first = generate_synthetic_transactions(500, seed=7)
    second = generate_synthetic_transactions(500, seed=7)
    pd.testing.assert_frame_equal(first, second)
    assert set(first["is_fraud"].unique()) == {0, 1}


def test_prepare_frame_rejects_missing_values():
    frame = generate_synthetic_transactions(300)
    frame.loc[0, "amount"] = None
    with pytest.raises(ValueError, match="Missing or non-finite"):
        prepare_frame(frame)


def test_threshold_and_calibration_are_bounded():
    y = np.array([0, 0, 0, 1, 1, 1])
    probability = np.array([0.05, 0.10, 0.20, 0.65, 0.80, 0.95])
    threshold = select_threshold(y, probability, minimum_recall=0.66)
    ece = expected_calibration_error(y, probability)
    assert 0 <= threshold <= 1
    assert 0 <= ece <= 1


def test_end_to_end_training_and_serialization(tmp_path: Path):
    X, y, _ = prepare_frame(generate_synthetic_transactions(1200, seed=11))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=11
    )
    result = train_candidate_models(X_train, y_train, seed=11, max_folds=3)
    probability = result.estimator.predict_proba(X_test)[:, 1]
    threshold = select_threshold(y_test, probability, minimum_recall=0.70)
    metrics = evaluate_binary_classifier(result.estimator, X_test, y_test, threshold)
    assert metrics["pr_auc"] > metrics["positive_rate"]
    assert 0 <= threshold <= 1

    path = save_model_bundle(result, threshold, tmp_path / "model.joblib")
    bundle = load_model_bundle(path)
    assert bundle["selected_model"] in {"logistic_regression", "random_forest"}
    assert bundle["feature_names"] == list(X.columns)
