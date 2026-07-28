#!/usr/bin/env python3
"""Build the reproducible Lead.AI customer-intelligence Kaggle notebook."""

from __future__ import annotations

from pathlib import Path
import uuid

import nbformat as nbf


OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "notebook"
    / "lead_ai_customer_intelligence_lab.ipynb"
)


def cell_id(index: int) -> str:
    return f"cell-{index:02d}-{uuid.uuid5(uuid.NAMESPACE_URL, str(index)).hex[:8]}"


def main() -> None:
    notebook = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            """# Lead.AI Customer Intelligence Lab
### Customer analytics, lead scoring, segmentation, and responsible AI

**Business hub:** [lead-ai.us](https://www.lead-ai.us)  
**GitHub:** [Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)  
**Dataset:** [Lead.AI Customer Intelligence Dataset](https://www.kaggle.com/datasets/arungharami/lead-ai-customer-intelligence-dataset)

This reproducible workflow validates data quality, explains business patterns, trains an interpretable lead-quality model, and creates advisory next-best actions.

> All rows are synthetic. Results are educational and must not be used as the sole basis for consequential customer decisions."""
        ),
        nbf.v4.new_code_cell(
            """from pathlib import Path
import warnings

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

warnings.filterwarnings("ignore")
RANDOM_STATE = 42
pd.set_option("display.max_columns", 50)
print("Environment ready.")"""
        ),
        nbf.v4.new_markdown_cell("## 1. Load the attached customer-intelligence dataset"),
        nbf.v4.new_code_cell(
            """paths = [
    Path("/kaggle/input/lead-ai-customer-intelligence-dataset/lead_ai_customer_intelligence.csv"),
    Path("../dataset/lead_ai_customer_intelligence.csv"),
    Path("kaggle/customer-intelligence/dataset/lead_ai_customer_intelligence.csv"),
]
data_path = next((path for path in paths if path.exists()), None)
if data_path is None:
    raise FileNotFoundError(
        "Attach arungharami/lead-ai-customer-intelligence-dataset "
        "or run this notebook from the repository."
    )

df = pd.read_csv(data_path)
print(f"Loaded {len(df):,} rows and {len(df.columns)} columns from {data_path}")
df.head()"""
        ),
        nbf.v4.new_markdown_cell("## 2. Data-quality contract"),
        nbf.v4.new_code_cell(
            """required = {
    "customer_id", "industry", "company_size", "acquisition_channel",
    "pipeline_stage", "monthly_revenue_usd", "marketing_spend_30d_usd",
    "website_sessions_30d", "leads_30d", "won_customers_30d",
    "conversion_rate_30d", "avg_response_time_hours", "crm_adoption_score",
    "automation_readiness_score", "engagement_score", "support_tickets_30d",
    "nps_score", "churn_risk_score", "lead_quality_score",
    "estimated_pipeline_value_usd", "recommended_segment",
    "next_best_action", "data_origin", "generated_at",
}
assert not (required - set(df.columns))
assert df["customer_id"].is_unique
assert df.isna().sum().sum() == 0
assert df["data_origin"].eq("synthetic").all()
assert df["conversion_rate_30d"].between(0, 1).all()
for column in [
    "crm_adoption_score", "automation_readiness_score", "engagement_score",
    "churn_risk_score", "lead_quality_score",
]:
    assert df[column].between(0, 100).all()
print("PASS: schema, IDs, missing values, origin, and score ranges.")"""
        ),
        nbf.v4.new_markdown_cell("## 3. Executive KPI snapshot and business segments"),
        nbf.v4.new_code_cell(
            """kpis = pd.Series({
    "Businesses represented": len(df),
    "Average leads (30d)": df["leads_30d"].mean(),
    "Average conversion rate": df["conversion_rate_30d"].mean(),
    "Average response time (hours)": df["avg_response_time_hours"].mean(),
    "Average automation readiness": df["automation_readiness_score"].mean(),
    "Average lead quality": df["lead_quality_score"].mean(),
    "Estimated pipeline value": df["estimated_pipeline_value_usd"].sum(),
})
display(kpis.to_frame("value"))

segments = (
    df.groupby("recommended_segment", as_index=False)
      .agg(
          businesses=("customer_id", "count"),
          avg_lead_quality=("lead_quality_score", "mean"),
          avg_churn_risk=("churn_risk_score", "mean"),
          avg_automation_readiness=("automation_readiness_score", "mean"),
          total_pipeline_value_usd=("estimated_pipeline_value_usd", "sum"),
      )
      .sort_values("total_pipeline_value_usd", ascending=False)
)
segments.round(2)"""
        ),
        nbf.v4.new_code_cell(
            """plot_data = segments.sort_values("total_pipeline_value_usd")
plt.figure(figsize=(10, 6))
plt.barh(plot_data["recommended_segment"], plot_data["total_pipeline_value_usd"])
plt.title("Estimated Pipeline Value by Lead.AI Segment")
plt.xlabel("Pipeline value (USD)")
plt.ylabel("Segment")
plt.tight_layout()
plt.show()"""
        ),
        nbf.v4.new_markdown_cell(
            """## 4. Interpretable lead-quality model

The target is synthetic, so the metrics demonstrate modeling mechanics rather than real-world predictive performance."""
        ),
        nbf.v4.new_code_cell(
            """target = "lead_quality_score"
features = [
    "industry", "company_size", "acquisition_channel", "pipeline_stage",
    "monthly_revenue_usd", "marketing_spend_30d_usd", "website_sessions_30d",
    "leads_30d", "conversion_rate_30d", "avg_response_time_hours",
    "crm_adoption_score", "automation_readiness_score", "engagement_score",
    "support_tickets_30d", "nps_score", "churn_risk_score",
]

X, y = df[features], df[target]
categorical = X.select_dtypes(include="object").columns.tolist()
numeric = [column for column in features if column not in categorical]

pipeline = Pipeline([
    ("preprocessor", ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", "passthrough", numeric),
    ])),
    ("model", RandomForestRegressor(
        n_estimators=300, min_samples_leaf=3,
        random_state=RANDOM_STATE, n_jobs=-1,
    )),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE
)
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)

pd.Series({
    "MAE": mean_absolute_error(y_test, predictions),
    "R²": r2_score(y_test, predictions),
}).to_frame("test_value")"""
        ),
        nbf.v4.new_markdown_cell("## 5. Explain the model with permutation importance"),
        nbf.v4.new_code_cell(
            """result = permutation_importance(
    pipeline, X_test, y_test, n_repeats=15,
    random_state=RANDOM_STATE, scoring="neg_mean_absolute_error",
)
importance = (
    pd.DataFrame({
        "feature": X_test.columns,
        "importance": result.importances_mean,
        "std": result.importances_std,
    })
    .sort_values("importance", ascending=False)
)
display(importance.head(10))

plot_data = importance.head(10).sort_values("importance")
plt.figure(figsize=(9, 6))
plt.barh(plot_data["feature"], plot_data["importance"])
plt.title("Top Drivers of Synthetic Lead-Quality Predictions")
plt.xlabel("Permutation importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()"""
        ),
        nbf.v4.new_markdown_cell("## 6. Next-best-action operating view"),
        nbf.v4.new_code_cell(
            """(
    df.sort_values(
        ["lead_quality_score", "estimated_pipeline_value_usd"],
        ascending=False,
    )
    .loc[:, [
        "customer_id", "industry", "company_size", "pipeline_stage",
        "lead_quality_score", "churn_risk_score",
        "automation_readiness_score", "estimated_pipeline_value_usd",
        "recommended_segment", "next_best_action",
    ]]
    .head(20)
)"""
        ),
        nbf.v4.new_markdown_cell(
            """## 7. Deployment and governance checklist

Before adapting this demonstration to real client data:

1. Obtain data-owner authorization and define lawful purpose.
2. Minimize fields and remove direct identifiers.
3. Document provenance, retention, access control, and incident response.
4. Validate outcomes across relevant groups and business segments.
5. Calibrate thresholds with domain experts and human-review workflows.
6. Monitor drift, false positives, false negatives, and operational impact.
7. Keep recommendations advisory unless production governance authorizes automation.

### Lead.AI ecosystem

- [lead-ai.us](https://www.lead-ai.us)
- [GitHub control center](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
- [Hugging Face organization](https://huggingface.co/lead-ai-labs)
- [Kaggle profile](https://www.kaggle.com/arungharami)"""
        ),
    ]

    for index, cell in enumerate(cells, start=1):
        cell["id"] = cell_id(index)

    notebook["cells"] = cells
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.11"},
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, OUTPUT_PATH)
    print(f"Built {len(cells)} cells at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
