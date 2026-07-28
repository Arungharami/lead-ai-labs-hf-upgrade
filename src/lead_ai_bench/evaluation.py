from __future__ import annotations

import time
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def select_threshold(
    y_true: pd.Series | np.ndarray,
    probability: np.ndarray,
    minimum_recall: float = 0.80,
) -> float:
    """Choose the highest-precision validation threshold meeting minimum recall."""
    if not 0 < minimum_recall <= 1:
        raise ValueError("minimum_recall must be in (0, 1]")
    precision, recall, thresholds = precision_recall_curve(y_true, probability)
    if len(thresholds) == 0:
        return 0.5

    candidates: list[tuple[float, float, float]] = []
    for index, threshold in enumerate(thresholds):
        if recall[index] >= minimum_recall:
            candidates.append((float(precision[index]), float(recall[index]), float(threshold)))
    if candidates:
        return max(candidates, key=lambda item: (item[0], item[2]))[2]

    f1 = 2 * precision[:-1] * recall[:-1] / np.clip(precision[:-1] + recall[:-1], 1e-12, None)
    return float(thresholds[int(np.nanargmax(f1))])


def expected_calibration_error(
    y_true: pd.Series | np.ndarray,
    probability: np.ndarray,
    bins: int = 10,
) -> float:
    y = np.asarray(y_true)
    probability = np.asarray(probability)
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for lower, upper in zip(edges[:-1], edges[1:]):
        mask = (probability >= lower) & (probability < upper if upper < 1 else probability <= upper)
        if not mask.any():
            continue
        ece += mask.mean() * abs(y[mask].mean() - probability[mask].mean())
    return float(ece)


def recall_at_max_fpr(
    y_true: pd.Series | np.ndarray,
    probability: np.ndarray,
    max_fpr: float = 0.01,
) -> float:
    fpr, tpr, _ = roc_curve(y_true, probability)
    eligible = tpr[fpr <= max_fpr]
    return float(eligible.max()) if len(eligible) else 0.0


def evaluate_binary_classifier(
    estimator: Any,
    X: pd.DataFrame,
    y_true: pd.Series,
    threshold: float,
    latency_repeats: int = 25,
) -> dict[str, Any]:
    probability = estimator.predict_proba(X)[:, 1]
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()

    sample = X.iloc[: min(128, len(X))]
    start = time.perf_counter()
    for _ in range(latency_repeats):
        estimator.predict_proba(sample)
    elapsed = time.perf_counter() - start
    per_row_ms = elapsed * 1000 / (latency_repeats * len(sample))

    return {
        "rows": int(len(X)),
        "positive_rate": float(np.mean(y_true)),
        "threshold": float(threshold),
        "pr_auc": float(average_precision_score(y_true, probability)),
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, prediction)),
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall": float(recall_score(y_true, prediction, zero_division=0)),
        "f1": float(f1_score(y_true, prediction, zero_division=0)),
        "mcc": float(matthews_corrcoef(y_true, prediction)),
        "brier_score": float(brier_score_loss(y_true, probability)),
        "expected_calibration_error": expected_calibration_error(y_true, probability),
        "recall_at_fpr_1pct": recall_at_max_fpr(y_true, probability, 0.01),
        "latency_ms_per_row": float(per_row_ms),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }
