import gradio as gr
import pandas as pd
import numpy as np

def calculate_fraud_risk(
    amount: float,
    transaction_hour: int,
    merchant_risk_score: float,
    customer_age_days: int,
    device_trust_score: float,
    location_risk_score: float,
    velocity_24h: int,
    previous_chargebacks: int,
    payment_method_risk: float
):
    """
    Explainable Fraud Risk Scoring Algorithm (Lead.AI Fraud Shield Engine)
    Computes marginal feature contributions and outputs risk percentage,
    level, XAI explanation breakdown, and business action.
    """

    # Base baseline risk (5%)
    base_risk = 0.05
    contributions = []

    # 1. Amount factor
    if amount > 2500:
        amt_contrib = +0.22
        contributions.append(("Transaction Amount", amt_contrib, f"High amount (${amount:,.2f}) increases risk"))
    elif amount > 750:
        amt_contrib = +0.10
        contributions.append(("Transaction Amount", amt_contrib, f"Moderate amount (${amount:,.2f})"))
    else:
        amt_contrib = -0.04
        contributions.append(("Transaction Amount", amt_contrib, f"Low standard amount (${amount:,.2f})"))

    # 2. Transaction Hour (Night time anomaly 11 PM - 5 AM)
    if transaction_hour in [23, 0, 1, 2, 3, 4]:
        hour_contrib = +0.12
        contributions.append(("Transaction Hour", hour_contrib, f"Late night hour ({transaction_hour}:00)"))
    else:
        hour_contrib = -0.02
        contributions.append(("Transaction Hour", hour_contrib, f"Normal business hour ({transaction_hour}:00)"))

    # 3. Merchant Category Risk
    merchant_contrib = (merchant_risk_score - 0.3) * 0.25
    contributions.append(("Merchant Risk", merchant_contrib, f"Merchant category risk index ({merchant_risk_score:.2f})"))

    # 4. Customer Account Age
    if customer_age_days < 14:
        age_contrib = +0.18
        contributions.append(("Customer History", age_contrib, f"New account age ({customer_age_days} days)"))
    elif customer_age_days < 90:
        age_contrib = +0.05
        contributions.append(("Customer History", age_contrib, f"Recent account ({customer_age_days} days)"))
    else:
        age_contrib = -0.12
        contributions.append(("Customer History", age_contrib, f"Established account ({customer_age_days} days)"))

    # 5. Device Trust Score
    device_contrib = (0.7 - device_trust_score) * 0.30
    if device_trust_score < 0.3:
        contributions.append(("Device Fingerprint", device_contrib, f"Untrusted device/IP score ({device_trust_score:.2f})"))
    else:
        contributions.append(("Device Fingerprint", device_contrib, f"Verified device score ({device_trust_score:.2f})"))

    # 6. Location Risk Score
    loc_contrib = (location_risk_score - 0.25) * 0.25
    if location_risk_score > 0.6:
        contributions.append(("Location Risk", loc_contrib, f"High geo-anomaly / proxy risk ({location_risk_score:.2f})"))
    else:
        contributions.append(("Location Risk", loc_contrib, f"Standard geo-location ({location_risk_score:.2f})"))

    # 7. Velocity 24h
    if velocity_24h > 10:
        vel_contrib = +0.25
        contributions.append(("24h Velocity", vel_contrib, f"Extreme transaction velocity ({velocity_24h} attempts/24h)"))
    elif velocity_24h > 4:
        vel_contrib = +0.10
        contributions.append(("24h Velocity", vel_contrib, f"Elevated velocity ({velocity_24h} attempts/24h)"))
    else:
        vel_contrib = -0.05
        contributions.append(("24h Velocity", vel_contrib, f"Normal velocity ({velocity_24h} attempt/24h)"))

    # 8. Previous Chargebacks
    cb_contrib = min(previous_chargebacks * 0.15, 0.40)
    if previous_chargebacks > 0:
        contributions.append(("Chargeback History", cb_contrib, f"{previous_chargebacks} prior chargeback record(s)"))

    # 9. Payment Method Risk
    pay_contrib = (payment_method_risk - 0.25) * 0.18
    contributions.append(("Payment Method", pay_contrib, f"Payment method risk weighting ({payment_method_risk:.2f})"))

    # Calculate Total Raw Score
    total_raw = base_risk + sum(c[1] for c in contributions)
    # Apply Sigmoid-style bounding between 1% and 99%
    risk_score_pct = float(np.clip(total_raw * 100, 1.0, 99.5))

    # Classification & Action Mapping
    if risk_score_pct >= 70.0:
        prediction_label = "🚨 HIGH FRAUD RISK"
        risk_level = "HIGH RISK"
        recommendation = "🛑 **DECLINE TRANSACTION & REASON:** High anomaly signals detected. Route to fraud team or require immediate identity re-verification."
    elif risk_score_pct >= 30.0:
        prediction_label = "⚠️ MODERATE FRAUD RISK"
        risk_level = "MODERATE RISK"
        recommendation = "🔍 **STEP-UP VERIFICATION:** Challenge transaction with 3D Secure / OTP SMS verification before fulfillment."
    else:
        prediction_label = "✅ LEGITIMATE TRANSACTION"
        risk_level = "LOW RISK"
        recommendation = "⚡ **AUTO-APPROVE:** Low risk parameters verified. Transaction cleared for real-time authorization."

    # Build XAI Markdown Report
    sorted_contribs = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)
    
    xai_md = "### 🔬 Feature Impact Breakdown (Explainable AI Attribution)\n\n"
    xai_md += "| Risk Factor | Impact Weight | Context Explanation |\n"
    xai_md += "| :--- | :--- | :--- |\n"
    for factor, weight, desc in sorted_contribs:
        direction = "📈 +{:.1f}% Risk".format(weight * 100) if weight > 0 else "📉 {:.1f}% Safety".format(weight * 100)
        xai_md += f"| **{factor}** | `{direction}` | {desc} |\n"

    xai_md += f"\n*Base System Baseline Risk: 5.0%*"

    return prediction_label, f"{risk_score_pct:.1f}%", risk_level, xai_md, recommendation


# Gradio Custom Theme Styling
theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme, title="Lead.AI Fraud Shield — Explainable Risk Engine") as demo:
    gr.Markdown(
        """
        # 🛡️ Lead.AI Fraud Shield — Explainable Fraud Detection Demo
        ### *Trustworthy AI, Risk Scoring & Explainability for Business Workflows*
        
        Powered by **[Lead.AI Labs](https://www.lead-ai.us)** | Founded by **Arun Kumar Gharami**
        
        Adjust the transaction parameters below to evaluate real-time fraud probability and receive instant **Explainable AI (XAI)** feature attributions.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Transaction Parameters")
            amount = gr.Number(label="Transaction Amount ($)", value=1250.00, precision=2)
            transaction_hour = gr.Slider(label="Transaction Hour (0-23)", minimum=0, maximum=23, step=1, value=3)
            merchant_risk_score = gr.Slider(label="Merchant Risk Score (0.0=Safe, 1.0=High)", minimum=0.0, maximum=1.0, step=0.01, value=0.85)
            customer_age_days = gr.Number(label="Customer Account Age (Days)", value=12, precision=0)
            device_trust_score = gr.Slider(label="Device Trust Score (0.0=Untrusted, 1.0=Verified)", minimum=0.0, maximum=1.0, step=0.01, value=0.15)
            location_risk_score = gr.Slider(label="Location / Geo Anomaly Score (0.0-1.0)", minimum=0.0, maximum=1.0, step=0.01, value=0.88)
            velocity_24h = gr.Slider(label="24-Hour Attempt Velocity", minimum=1, maximum=30, step=1, value=14)
            previous_chargebacks = gr.Number(label="Previous Chargeback Count", value=2, precision=0)
            payment_method_risk = gr.Slider(label="Payment Method Risk Index (0.0-1.0)", minimum=0.0, maximum=1.0, step=0.01, value=0.80)

            submit_btn = gr.Button("🛡️ Calculate Fraud Risk & Generate XAI Breakdown", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 📤 Real-Time Risk Analysis")
            pred_output = gr.Textbox(label="Prediction Status", interactive=False)
            
            with gr.Row():
                score_output = gr.Textbox(label="Calculated Risk Score", interactive=False)
                level_output = gr.Textbox(label="Risk Tier", interactive=False)

            rec_output = gr.Markdown(label="Business Action Recommendation")
            xai_output = gr.Markdown(label="Explainable AI Breakdown")

    # Sample Presets
    gr.Examples(
        examples=[
            [45.20, 14, 0.15, 450, 0.92, 0.10, 2, 0, 0.15],
            [1250.00, 3, 0.85, 12, 0.15, 0.88, 14, 2, 0.80],
            [3200.00, 23, 0.65, 5, 0.20, 0.75, 18, 1, 0.70]
        ],
        inputs=[
            amount, transaction_hour, merchant_risk_score, customer_age_days,
            device_trust_score, location_risk_score, velocity_24h,
            previous_chargebacks, payment_method_risk
        ],
        outputs=[pred_output, score_output, level_output, xai_output, rec_output],
        fn=calculate_fraud_risk,
        cache_examples=False
    )

    submit_btn.click(
        fn=calculate_fraud_risk,
        inputs=[
            amount, transaction_hour, merchant_risk_score, customer_age_days,
            device_trust_score, location_risk_score, velocity_24h,
            previous_chargebacks, payment_method_risk
        ],
        outputs=[pred_output, score_output, level_output, xai_output, rec_output]
    )

    gr.Markdown(
        """
        ---
        ### 🌐 Integrate Lead.AI Fraud Shield into Your Business Workflow
        Need custom explainable fraud detection models trained on your private enterprise data?
        * 🔗 **Official Website:** [www.lead-ai.us](https://www.lead-ai.us)
        * 💻 **GitHub Control Center:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade)
        * 📂 **Hugging Face Organization:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs)
        
        *Disclaimer: Synthetic demonstration model for portfolio, research, and product prototyping.*
        """
    )

if __name__ == "__main__":
    demo.launch()
