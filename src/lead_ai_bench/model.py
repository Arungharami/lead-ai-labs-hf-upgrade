from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class CandidateScore:
    name: str
    pr_auc_mean: float
    roc_auc_mean: float


@dataclass
class TrainingResult:
    estimator: BaseEstimator
    selected_model: str
    candidate_scores: list[CandidateScore]
    feature_names: list[str]


def _candidates(seed: int) -> dict[str, BaseEstimator]:
    return {
        "logistic_regression": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=2000,
                        random_state=seed,
                    ),
                ),
            ]
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=350,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=seed,
        ),
    }


def train_candidate_models(
    X: pd.DataFrame,
    y: pd.Series,
    seed: int = 42,
    max_folds: int = 5,
) -> TrainingResult:
    """Select a model using out-of-fold PR-AUC, then refit on all training rows."""
    if len(X) != len(y):
        raise ValueError("X and y lengths differ")
    folds = min(max_folds, int(y.value_counts().min()))
    if folds < 2:
        raise ValueError("At least two stratified folds are required")
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)

    scores: list[CandidateScore] = []
    fitted: dict[str, BaseEstimator] = {}
    for name, estimator in _candidates(seed).items():
        oof_probability = cross_val_predict(
            estimator,
            X,
            y,
            cv=cv,
            method="predict_proba",
            n_jobs=-1,
        )[:, 1]
        pr_auc = float(average_precision_score(y, oof_probability))
        roc_auc = float(roc_auc_score(y, oof_probability))
        scores.append(CandidateScore(name, pr_auc, roc_auc))
        fitted[name] = estimator

    winner = max(scores, key=lambda item: (item.pr_auc_mean, item.roc_auc_mean)).name
    estimator = fitted[winner]
    estimator.fit(X, y)
    return TrainingResult(estimator, winner, scores, list(X.columns))


def save_model_bundle(
    result: TrainingResult,
    threshold: float,
    output_path: str | Path,
    metadata: dict[str, Any] | None = None,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "estimator": result.estimator,
        "feature_names": result.feature_names,
        "threshold": float(threshold),
        "selected_model": result.selected_model,
        "candidate_scores": [score.__dict__ for score in result.candidate_scores],
        "metadata": metadata or {},
    }
    joblib.dump(bundle, output_path)
    return output_path


def load_model_bundle(path: str | Path) -> dict[str, Any]:
    bundle = joblib.load(path)
    required = {"estimator", "feature_names", "threshold", "selected_model"}
    missing = required.difference(bundle)
    if missing:
        raise ValueError(f"Invalid model bundle; missing keys: {sorted(missing)}")
    return bundle


def predict_bundle(bundle: dict[str, Any], records: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    features = list(bundle["feature_names"])
    missing = [column for column in features if column not in records.columns]
    if missing:
        raise ValueError(f"Prediction input missing features: {missing}")
    probability = bundle["estimator"].predict_proba(records[features])[:, 1]
    label = (probability >= float(bundle["threshold"])).astype(int)
    return probability, label
