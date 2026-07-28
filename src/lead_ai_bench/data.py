from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

TARGET_CANDIDATES = ("is_fraud", "Class", "class", "label", "target")
ID_CANDIDATES = ("transaction_id", "id", "ID")


def generate_synthetic_transactions(n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate auditable synthetic transactions with probabilistic labels.

    The generator is intentionally stochastic instead of using a hard label rule. This
    prevents a model from achieving artificial 100% accuracy while keeping feature/label
    relationships interpretable for demos and CI.
    """
    if n_rows < 200:
        raise ValueError("n_rows must be at least 200 for stable stratified evaluation")

    rng = np.random.default_rng(seed)
    amount = np.clip(rng.lognormal(mean=5.25, sigma=1.05, size=n_rows), 1, 10000)
    transaction_hour = rng.integers(0, 24, size=n_rows)
    merchant_risk_score = rng.beta(2.0, 4.0, size=n_rows)
    customer_age_days = np.clip(rng.gamma(2.2, 260, size=n_rows), 1, 3000).astype(int)
    device_trust_score = rng.beta(4.5, 2.0, size=n_rows)
    location_risk_score = rng.beta(1.8, 4.2, size=n_rows)
    velocity_24h = np.clip(rng.poisson(3.5, size=n_rows) + 1, 1, 40)
    previous_chargebacks = np.clip(rng.poisson(0.25, size=n_rows), 0, 8)
    payment_method_risk = rng.beta(2.0, 4.0, size=n_rows)

    night = np.isin(transaction_hour, [23, 0, 1, 2, 3, 4]).astype(float)
    linear_risk = (
        -7.0
        + 0.00135 * amount
        + 5.40 * merchant_risk_score
        - 5.40 * device_trust_score
        + 5.40 * location_risk_score
        + 0.324 * velocity_24h
        + 1.98 * previous_chargebacks
        + 3.96 * payment_method_risk
        + 1.98 * night
        - 0.00216 * customer_age_days
        + rng.normal(0, 0.20, size=n_rows)
    )
    fraud_probability = 1.0 / (1.0 + np.exp(-linear_risk))
    is_fraud = rng.binomial(1, fraud_probability)

    # Guarantee both classes for very unlucky seeds.
    if is_fraud.sum() < 20:
        is_fraud[np.argsort(fraud_probability)[-20:]] = 1
    if (is_fraud == 0).sum() < 20:
        is_fraud[np.argsort(fraud_probability)[:20]] = 0

    return pd.DataFrame(
        {
            "transaction_id": [f"SYN-{seed}-{i:07d}" for i in range(n_rows)],
            "amount": amount.round(2),
            "transaction_hour": transaction_hour,
            "merchant_risk_score": merchant_risk_score.round(5),
            "customer_age_days": customer_age_days,
            "device_trust_score": device_trust_score.round(5),
            "location_risk_score": location_risk_score.round(5),
            "velocity_24h": velocity_24h,
            "previous_chargebacks": previous_chargebacks,
            "payment_method_risk": payment_method_risk.round(5),
            "is_fraud": is_fraud,
        }
    )


def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def load_huggingface_dataset(
    repo_id: str = "lead-ai-labs/fraud-detection-Table-data",
    split: str = "train",
) -> pd.DataFrame:
    """Load a Hub dataset without making datasets a mandatory dependency."""
    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("Install with: pip install -e '.[huggingface]'") from exc
    return load_dataset(repo_id, split=split).to_pandas()


def infer_target_column(frame: pd.DataFrame, requested: str | None = None) -> str:
    if requested:
        if requested not in frame.columns:
            raise ValueError(f"Target column '{requested}' is missing")
        return requested
    for column in TARGET_CANDIDATES:
        if column in frame.columns:
            return column
    raise ValueError(f"No binary target found. Tried: {', '.join(TARGET_CANDIDATES)}")


def prepare_frame(
    frame: pd.DataFrame,
    target_column: str | None = None,
    id_columns: Iterable[str] = ID_CANDIDATES,
) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Validate a binary tabular dataset and return numeric X/y.

    Text identifiers are excluded. All remaining feature columns must be numeric and finite.
    Duplicate rows are removed before training to reduce leakage.
    """
    if frame.empty:
        raise ValueError("Dataset is empty")

    clean = frame.copy().drop_duplicates().reset_index(drop=True)
    target = infer_target_column(clean, target_column)
    clean[target] = pd.to_numeric(clean[target], errors="raise").astype(int)
    unique = set(clean[target].dropna().unique().tolist())
    if not unique.issubset({0, 1}) or len(unique) != 2:
        raise ValueError(f"Target must contain both binary classes 0 and 1; found {sorted(unique)}")

    excluded = {target, *[c for c in id_columns if c in clean.columns]}
    feature_names = [c for c in clean.columns if c not in excluded]
    if not feature_names:
        raise ValueError("No feature columns remain after excluding identifiers and target")

    X = clean[feature_names].apply(pd.to_numeric, errors="raise").astype(float)
    X = X.replace([np.inf, -np.inf], np.nan)
    if X.isna().any().any():
        missing = X.columns[X.isna().any()].tolist()
        raise ValueError(f"Missing or non-finite feature values in: {missing}")

    y = clean[target].astype(int)
    minority = int(y.value_counts().min())
    if minority < 10:
        raise ValueError("Each class needs at least 10 rows for defensible stratified evaluation")
    return X, y, feature_names
