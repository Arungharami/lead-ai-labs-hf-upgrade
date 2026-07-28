"""Deterministic Kaggle benchmark for auditable fraud-policy reasoning.

The model sees the exact scoring policy. Expected decisions, scores, and reason
codes are computed in code; no LLM judge is used.
"""

from __future__ import annotations

import json
import re
from typing import Any

import kaggle_benchmarks as kbench

TASK_NAME = "lead-ai-fraud-policy-reasoning"
ALLOWED_DECISIONS = {"APPROVE", "REVIEW", "DECLINE"}
ALLOWED_REASONS = {
    "HIGH_AMOUNT", "NIGHT_TRANSACTION", "HIGH_MERCHANT_RISK", "NEW_ACCOUNT",
    "UNTRUSTED_DEVICE", "HIGH_LOCATION_RISK", "HIGH_VELOCITY",
    "PRIOR_CHARGEBACKS", "HIGH_PAYMENT_METHOD_RISK", "LOW_RISK_PROFILE",
}
FORBIDDEN_ATTRIBUTES = re.compile(
    r"\b(race|ethnicity|religion|gender|sex|nationality|disability|marital status)\b",
    re.IGNORECASE,
)

POLICY_TEXT = """
Apply this deterministic policy exactly.
Risk points, using only the highest matching tier in each category:
1. amount >= 3000: +15; else amount >= 1000: +8.
2. transaction_hour 0 through 5: +12.
3. merchant_risk_score >= 0.75: +18; else >= 0.50: +10.
4. customer_age_days <= 30: +15; else <= 90: +8.
5. device_trust_score <= 0.25: +20; else <= 0.50: +12.
6. location_risk_score >= 0.75: +18; else >= 0.50: +10.
7. velocity_24h >= 15: +18; else >= 8: +10.
8. previous_chargebacks >= 2: +18; else >= 1: +10.
9. payment_method_risk >= 0.75: +15; else >= 0.50: +8.
Clamp the total to 0-100. APPROVE=0-29, REVIEW=30-69, DECLINE=70-100.
Return the two highest-point triggered reason codes; break ties by the category
order above. If nothing triggers, return LOW_RISK_PROFILE. Do not use or mention
protected or sensitive personal attributes.
""".strip()

CASES: tuple[dict[str, Any], ...] = (
    {"id":"A01","amount":42.5,"transaction_hour":14,"merchant_risk_score":0.10,"customer_age_days":800,"device_trust_score":0.95,"location_risk_score":0.08,"velocity_24h":2,"previous_chargebacks":0,"payment_method_risk":0.12},
    {"id":"A02","amount":1200.0,"transaction_hour":10,"merchant_risk_score":0.18,"customer_age_days":1200,"device_trust_score":0.90,"location_risk_score":0.12,"velocity_24h":3,"previous_chargebacks":0,"payment_method_risk":0.15},
    {"id":"A03","amount":1100.0,"transaction_hour":3,"merchant_risk_score":0.22,"customer_age_days":600,"device_trust_score":0.88,"location_risk_score":0.15,"velocity_24h":2,"previous_chargebacks":0,"payment_method_risk":0.20},
    {"id":"A04","amount":315.2,"transaction_hour":16,"merchant_risk_score":0.55,"customer_age_days":60,"device_trust_score":0.88,"location_risk_score":0.15,"velocity_24h":2,"previous_chargebacks":0,"payment_method_risk":0.55},
    {"id":"A05","amount":89.0,"transaction_hour":9,"merchant_risk_score":0.20,"customer_age_days":91,"device_trust_score":0.80,"location_risk_score":0.20,"velocity_24h":7,"previous_chargebacks":0,"payment_method_risk":0.49},
    {"id":"R01","amount":780.0,"transaction_hour":3,"merchant_risk_score":0.48,"customer_age_days":60,"device_trust_score":0.45,"location_risk_score":0.41,"velocity_24h":7,"previous_chargebacks":0,"payment_method_risk":0.42},
    {"id":"R02","amount":1200.0,"transaction_hour":20,"merchant_risk_score":0.55,"customer_age_days":120,"device_trust_score":0.80,"location_risk_score":0.52,"velocity_24h":8,"previous_chargebacks":0,"payment_method_risk":0.20},
    {"id":"R03","amount":3400.0,"transaction_hour":8,"merchant_risk_score":0.20,"customer_age_days":150,"device_trust_score":0.80,"location_risk_score":0.20,"velocity_24h":4,"previous_chargebacks":1,"payment_method_risk":0.55},
    {"id":"R04","amount":650.0,"transaction_hour":23,"merchant_risk_score":0.75,"customer_age_days":25,"device_trust_score":0.49,"location_risk_score":0.20,"velocity_24h":5,"previous_chargebacks":0,"payment_method_risk":0.20},
    {"id":"R05","amount":1900.0,"transaction_hour":8,"merchant_risk_score":0.62,"customer_age_days":150,"device_trust_score":0.44,"location_risk_score":0.55,"velocity_24h":9,"previous_chargebacks":0,"payment_method_risk":0.65},
    {"id":"D01","amount":3400.0,"transaction_hour":2,"merchant_risk_score":0.88,"customer_age_days":8,"device_trust_score":0.12,"location_risk_score":0.91,"velocity_24h":22,"previous_chargebacks":3,"payment_method_risk":0.90},
    {"id":"D02","amount":2700.0,"transaction_hour":1,"merchant_risk_score":0.75,"customer_age_days":20,"device_trust_score":0.20,"location_risk_score":0.82,"velocity_24h":8,"previous_chargebacks":1,"payment_method_risk":0.77},
    {"id":"D03","amount":4600.0,"transaction_hour":22,"merchant_risk_score":0.55,"customer_age_days":200,"device_trust_score":0.45,"location_risk_score":0.55,"velocity_24h":8,"previous_chargebacks":3,"payment_method_risk":0.55},
    {"id":"D04","amount":1500.0,"transaction_hour":4,"merchant_risk_score":0.93,"customer_age_days":12,"device_trust_score":0.16,"location_risk_score":0.60,"velocity_24h":9,"previous_chargebacks":0,"payment_method_risk":0.55},
    {"id":"D05","amount":2200.0,"transaction_hour":15,"merchant_risk_score":0.49,"customer_age_days":60,"device_trust_score":0.20,"location_risk_score":0.80,"velocity_24h":16,"previous_chargebacks":1,"payment_method_risk":0.20},
)


def _risk_components(case: dict[str, Any]) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    def add(code: str, points: int) -> None:
        if points:
            out.append((code, points))
    add("HIGH_AMOUNT", 15 if case["amount"] >= 3000 else 8 if case["amount"] >= 1000 else 0)
    add("NIGHT_TRANSACTION", 12 if 0 <= case["transaction_hour"] <= 5 else 0)
    add("HIGH_MERCHANT_RISK", 18 if case["merchant_risk_score"] >= .75 else 10 if case["merchant_risk_score"] >= .50 else 0)
    add("NEW_ACCOUNT", 15 if case["customer_age_days"] <= 30 else 8 if case["customer_age_days"] <= 90 else 0)
    add("UNTRUSTED_DEVICE", 20 if case["device_trust_score"] <= .25 else 12 if case["device_trust_score"] <= .50 else 0)
    add("HIGH_LOCATION_RISK", 18 if case["location_risk_score"] >= .75 else 10 if case["location_risk_score"] >= .50 else 0)
    add("HIGH_VELOCITY", 18 if case["velocity_24h"] >= 15 else 10 if case["velocity_24h"] >= 8 else 0)
    add("PRIOR_CHARGEBACKS", 18 if case["previous_chargebacks"] >= 2 else 10 if case["previous_chargebacks"] >= 1 else 0)
    add("HIGH_PAYMENT_METHOD_RISK", 15 if case["payment_method_risk"] >= .75 else 8 if case["payment_method_risk"] >= .50 else 0)
    return out


def _expected(case: dict[str, Any]) -> tuple[int, str, list[str]]:
    components = _risk_components(case)
    score = min(100, sum(points for _, points in components))
    decision = "APPROVE" if score <= 29 else "REVIEW" if score <= 69 else "DECLINE"
    ranked = sorted(enumerate(components), key=lambda item: (-item[1][1], item[0]))
    reasons = [entry[1][0] for entry in ranked[:2]] if ranked else ["LOW_RISK_PROFILE"]
    return score, decision, reasons


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end < start:
        return {}
    try:
        value = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _reason_f1(expected: list[str], predicted: Any) -> float:
    if not isinstance(predicted, list):
        return 0.0
    expected_set = set(expected)
    predicted_set = {str(x).strip().upper() for x in predicted if str(x).strip().upper() in ALLOWED_REASONS}
    if not predicted_set:
        return 0.0
    overlap = len(expected_set & predicted_set)
    precision, recall = overlap / len(predicted_set), overlap / len(expected_set)
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def _score_response(response: str, case: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    expected_score, expected_decision, expected_reasons = _expected(case)
    parsed = _parse_json(response)
    decision = str(parsed.get("decision", "")).strip().upper()
    raw_score = parsed.get("risk_score")
    risk_score = raw_score if isinstance(raw_score, int) and not isinstance(raw_score, bool) else None
    explanation = parsed.get("explanation")
    schema_ok = (
        set(parsed) == {"decision", "risk_score", "reason_codes", "explanation"}
        and decision in ALLOWED_DECISIONS and risk_score is not None and 0 <= risk_score <= 100
        and isinstance(parsed.get("reason_codes"), list)
        and isinstance(explanation, str) and bool(explanation.strip())
    )
    error = abs(risk_score - expected_score) if risk_score is not None else 101
    score_component = 1.0 if error <= 2 else .75 if error <= 5 else .4 if error <= 10 else 0.0
    reason_component = _reason_f1(expected_reasons, parsed.get("reason_codes"))
    details = {
        "schema_ok": schema_ok,
        "decision_ok": decision == expected_decision,
        "score_error": error,
        "reasons_f1": reason_component,
        "safety_ok": FORBIDDEN_ATTRIBUTES.search(response) is None,
    }
    total = .15*details["schema_ok"] + .30*details["decision_ok"] + .25*score_component + .20*reason_component + .10*details["safety_ok"]
    return total, details


def _build_prompt(case: dict[str, Any]) -> str:
    transaction = "\n".join(f"- {key}: {value}" for key, value in case.items() if key != "id")
    return f"""You are an auditable financial fraud-risk decision-support model.

{POLICY_TEXT}

Transaction case {case['id']}:
{transaction}

Return exactly one JSON object and no markdown:
{{"decision":"APPROVE|REVIEW|DECLINE","risk_score":0,"reason_codes":["UPPER_SNAKE_CASE"],"explanation":"one concise numeric-signal-based sentence"}}"""


@kbench.task(
    name=TASK_NAME,
    description="Apply a disclosed fraud policy with deterministic scoring and grounded JSON decisions.",
    version=2,
)
def fraud_policy_reasoning(llm) -> float:
    scores: list[float] = []
    for index, case in enumerate(CASES):
        with kbench.chats.new(f"fraud_policy_case_{index:02d}"):
            response = str(llm.prompt(_build_prompt(case)))
        score, details = _score_response(response, case)
        scores.append(score)
        kbench.assertions.assert_true(details["schema_ok"], expectation=f"{case['id']}: return the exact JSON contract.")
        kbench.assertions.assert_true(details["decision_ok"], expectation=f"{case['id']}: apply decision thresholds correctly.")
        kbench.assertions.assert_true(details["score_error"] <= 5, expectation=f"{case['id']}: calculate risk within five points.")
        kbench.assertions.assert_true(details["reasons_f1"] >= .8, expectation=f"{case['id']}: identify the strongest reasons.")
        kbench.assertions.assert_true(details["safety_ok"], expectation=f"{case['id']}: omit protected attributes.")
    return round(sum(scores) / len(scores), 6)
