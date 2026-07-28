from __future__ import annotations

import importlib.util
import json
import re
import sys
import types
from contextlib import nullcontext
from pathlib import Path


class _TaskDecorator:
    def __call__(self, *args, **kwargs):
        def decorate(function):
            function.task_metadata = kwargs
            return function
        return decorate


class _Assertions:
    @staticmethod
    def assert_true(condition, expectation=None):
        return bool(condition)


_STUB = types.ModuleType("kaggle_benchmarks")
_STUB.task = _TaskDecorator()
_STUB.assertions = _Assertions()
_STUB.chats = types.SimpleNamespace(new=lambda name: nullcontext())
sys.modules.setdefault("kaggle_benchmarks", _STUB)

ROOT = Path(__file__).resolve().parents[1] / "kaggle" / "benchmarks"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


policy = _load("fraud_risk_reasoning")
safety = _load("fraud_adversarial_safety")
uncertainty = _load("fraud_uncertainty_escalation")


class _PolicyLLM:
    def prompt(self, prompt: str) -> str:
        case_id = re.search(r"Transaction case ([A-Z]\d+):", prompt).group(1)
        case = next(item for item in policy.CASES if item["id"] == case_id)
        score, decision, reasons = policy._expected(case)
        return json.dumps({
            "decision": decision,
            "risk_score": score,
            "reason_codes": reasons,
            "explanation": f"Numeric signals produce a risk score of {score}.",
        })


class _SafetyLLM:
    def prompt(self, prompt: str) -> str:
        case_id = re.search(r"signals for ([A-Z]\d+):", prompt).group(1)
        case = next(item for item in safety.CASES if item["id"] == case_id)
        score = safety._score(case)
        return json.dumps({
            "decision": safety._decision(score),
            "risk_score": score,
            "note_ignored": True,
            "explanation": f"Trusted numeric signals produce a risk score of {score}.",
        })


class _UncertaintyLLM:
    def prompt(self, prompt: str) -> str:
        case_id = re.search(r"Transaction case ([A-Z]\d+):", prompt).group(1)
        case = next(item for item in uncertainty.CASES if item["id"] == case_id)
        issue = case["expected_issue"]
        field = issue.replace("MISSING_", "").replace("INVALID_", "").lower()
        return json.dumps({
            "decision": "REVIEW",
            "risk_score": None,
            "needs_human_review": True,
            "issue_code": issue,
            "explanation": f"The {field} field is missing or invalid.",
        })


def test_reference_models_score_one() -> None:
    assert policy.fraud_policy_reasoning(_PolicyLLM()) == 1.0
    assert safety.fraud_adversarial_safety(_SafetyLLM()) == 1.0
    assert uncertainty.fraud_uncertainty_escalation(_UncertaintyLLM()) == 1.0


def test_policy_cases_are_balanced() -> None:
    labels = [policy._expected(case)[1] for case in policy.CASES]
    assert labels.count("APPROVE") == 5
    assert labels.count("REVIEW") == 5
    assert labels.count("DECLINE") == 5


def test_invalid_json_does_not_pass_contract() -> None:
    score, details = policy._score_response("not json", policy.CASES[0])
    assert score < 0.5
    assert details["schema_ok"] is False
