"""Lead.AI fraud detection benchmark package."""

from .data import TARGET_CANDIDATES, generate_synthetic_transactions, prepare_frame
from .evaluation import evaluate_binary_classifier, select_threshold
from .model import load_model_bundle, save_model_bundle, train_candidate_models

__all__ = [
    "TARGET_CANDIDATES",
    "evaluate_binary_classifier",
    "generate_synthetic_transactions",
    "load_model_bundle",
    "prepare_frame",
    "save_model_bundle",
    "select_threshold",
    "train_candidate_models",
]
