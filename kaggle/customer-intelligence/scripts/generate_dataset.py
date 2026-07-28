#!/usr/bin/env python3
"""Generate the deterministic synthetic Lead.AI customer-intelligence dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_STATE = 42
ROW_COUNT = 500
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "dataset" / "lead_ai_customer_intelligence.csv"


def build_dataset(row_count: int = ROW_COUNT) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)

    industries = np.array([
        "Retail", "Professional Services", "Construction", "Healthcare",
        "Hospitality", "E-commerce", "Real Estate", "Education",
    ])
    company_sizes = np.array(["Micro", "Small", "Mid-market"])
    channels = np.array([
        "Organic Search", "Paid Search", "Referral", "Social", "Email", "Direct",
    ])
    stages = np.array([
        "New", "Qualified", "Discovery", "Proposal", "Negotiation", "Customer",
    ])

    industry = rng.choice(
        industries, size=row_count,
        p=[0.16, 0.17, 0.12, 0.10, 0.11, 0.15, 0.10, 0.09],
    )
    company_size = rng.choice(
        company_sizes, size=row_count, p=[0.46, 0.39, 0.15],
    )
    size_factor = (
        pd.Series(company_size)
        .map({"Micro": 0.65, "Small": 1.0, "Mid-market": 1.65})
        .to_numpy()
    )

    monthly_revenue = np.round(
        np.exp(rng.normal(np.log(42_000 * size_factor), 0.55)), 2
    )
    website_sessions = np.maximum(
        50, rng.gamma(4.2, 220, row_count) * size_factor
    ).astype(int)
    marketing_spend = np.round(
        np.maximum(250, monthly_revenue * rng.uniform(0.015, 0.095, row_count)), 2
    )
    leads = np.maximum(
        2, website_sessions * rng.uniform(0.012, 0.075, row_count)
    ).astype(int)
    response_hours = np.round(
        np.clip(rng.lognormal(mean=1.4, sigma=0.75, size=row_count), 0.2, 72), 2
    )
    crm_score = np.round(
        np.clip(
            rng.normal(
                58
                + 13 * (company_size == "Mid-market")
                - 8 * (company_size == "Micro"),
                18,
                row_count,
            ),
            0,
            100,
        ),
        1,
    )
    automation_score = np.round(
        np.clip(0.46 * crm_score + rng.normal(28, 16, row_count), 0, 100), 1
    )
    engagement = np.round(
        np.clip(
            0.22 * np.log1p(website_sessions) * 10
            + 0.25 * np.log1p(leads) * 10
            + 0.30 * crm_score
            + 0.23 * automation_score
            + rng.normal(0, 7, row_count),
            0,
            100,
        ),
        1,
    )
    conversion = np.round(
        np.clip(
            0.015
            + 0.00042 * engagement
            + 0.00023 * (72 - response_hours)
            + rng.normal(0, 0.012, row_count),
            0.005,
            0.22,
        ),
        4,
    )
    won_customers = np.minimum(
        leads, rng.binomial(leads, np.clip(conversion, 0, 1))
    )
    support_tickets = np.maximum(
        0,
        rng.poisson(np.clip(won_customers * 0.6 + size_factor * 1.4, 0.2, 25)),
    ).astype(int)
    nps = np.round(
        np.clip(
            28
            + 0.46 * automation_score
            + 0.24 * crm_score
            - 0.45 * response_hours
            + rng.normal(0, 16, row_count),
            -100,
            100,
        ),
        0,
    ).astype(int)
    churn = np.round(
        np.clip(
            74
            - 0.42 * nps
            - 0.20 * engagement
            + 0.30 * response_hours
            + rng.normal(0, 8, row_count),
            0,
            100,
        ),
        1,
    )
    lead_quality = np.round(
        np.clip(
            0.34 * engagement
            + 0.28 * automation_score
            + 0.22 * crm_score
            + 0.16 * (100 - churn)
            + rng.normal(0, 5, row_count),
            0,
            100,
        ),
        1,
    )
    pipeline_value = np.round(
        leads
        * np.clip(
            monthly_revenue * rng.uniform(0.008, 0.04, row_count),
            500,
            25_000,
        ),
        2,
    )

    segment = np.select(
        [
            (lead_quality >= 75) & (automation_score >= 65),
            lead_quality >= 60,
            churn >= 65,
            automation_score < 40,
        ],
        [
            "High-Intent Automation Buyer",
            "Growth Opportunity",
            "Retention Risk",
            "Digital Foundation Needed",
        ],
        default="Nurture",
    )
    action = np.select(
        [
            segment == "High-Intent Automation Buyer",
            segment == "Growth Opportunity",
            segment == "Retention Risk",
            segment == "Digital Foundation Needed",
        ],
        [
            "Schedule solution discovery and prepare ROI estimate",
            "Launch personalized nurture sequence and qualification call",
            "Prioritize customer-success outreach and service recovery",
            "Offer CRM and workflow readiness assessment",
        ],
        default="Continue educational nurture and monitor engagement",
    )

    return pd.DataFrame({
        "customer_id": [f"LAI-{index:05d}" for index in range(1, row_count + 1)],
        "industry": industry,
        "company_size": company_size,
        "acquisition_channel": rng.choice(channels, row_count),
        "pipeline_stage": rng.choice(
            stages, row_count, p=[0.18, 0.22, 0.18, 0.16, 0.10, 0.16]
        ),
        "monthly_revenue_usd": monthly_revenue,
        "marketing_spend_30d_usd": marketing_spend,
        "website_sessions_30d": website_sessions,
        "leads_30d": leads,
        "won_customers_30d": won_customers,
        "conversion_rate_30d": conversion,
        "avg_response_time_hours": response_hours,
        "crm_adoption_score": crm_score,
        "automation_readiness_score": automation_score,
        "engagement_score": engagement,
        "support_tickets_30d": support_tickets,
        "nps_score": nps,
        "churn_risk_score": churn,
        "lead_quality_score": lead_quality,
        "estimated_pipeline_value_usd": pipeline_value,
        "recommended_segment": segment,
        "next_best_action": action,
        "data_origin": "synthetic",
        "generated_at": "2026-07-27",
    })


def main() -> None:
    dataset = build_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(
        f"Generated {len(dataset)} rows and {len(dataset.columns)} columns at "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
