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
    Lead.AI Fraud Shield XAI Risk Engine
    Calculates transaction risk probability and generates quantitative 
    feature attribution metrics for explainable AI auditing.
    """

    base_risk = 0.05
    contributions = []

    # 1. Amount Factor
    if amount > 2500:
        amt_contrib = +0.22
        contributions.append(("Transaction Amount", amt_contrib, f"High transaction value (${amount:,.2f}) elevates loss exposure"))
    elif amount > 750:
        amt_contrib = +0.10
        contributions.append(("Transaction Amount", amt_contrib, f"Moderate transaction value (${amount:,.2f})"))
    else:
        amt_contrib = -0.04
        contributions.append(("Transaction Amount", amt_contrib, f"Standard low-risk amount (${amount:,.2f})"))

    # 2. Transaction Hour (Night anomaly)
    if transaction_hour in [23, 0, 1, 2, 3, 4]:
        hour_contrib = +0.12
        contributions.append(("Transaction Hour", hour_contrib, f"Late-night activity window ({transaction_hour}:00 hrs)"))
    else:
        hour_contrib = -0.02
        contributions.append(("Transaction Hour", hour_contrib, f"Normal daytime operating hour ({transaction_hour}:00 hrs)"))

    # 3. Merchant Risk Index
    merchant_contrib = (merchant_risk_score - 0.3) * 0.25
    contributions.append(("Merchant Category Risk", merchant_contrib, f"Merchant category risk index ({merchant_risk_score:.2f})"))

    # 4. Customer Account Age
    if customer_age_days < 14:
        age_contrib = +0.18
        contributions.append(("Customer Account Age", age_contrib, f"New unverified account ({customer_age_days} days old)"))
    elif customer_age_days < 90:
        age_contrib = +0.05
        contributions.append(("Customer Account Age", age_contrib, f"Recent account history ({customer_age_days} days old)"))
    else:
        age_contrib = -0.12
        contributions.append(("Customer Account Age", age_contrib, f"Established trusted tenure ({customer_age_days} days old)"))

    # 5. Device Trust Fingerprint
    device_contrib = (0.7 - device_trust_score) * 0.30
    if device_trust_score < 0.3:
        contributions.append(("Device Trust Score", device_contrib, f"Untrusted device fingerprint / proxy IP ({device_trust_score:.2f})"))
    else:
        contributions.append(("Device Trust Score", device_contrib, f"Verified hardware fingerprint ({device_trust_score:.2f})"))

    # 6. Location Risk Score
    loc_contrib = (location_risk_score - 0.25) * 0.25
    if location_risk_score > 0.6:
        contributions.append(("Geo-Location Anomaly", loc_contrib, f"High geo-mismatch / VPN risk score ({location_risk_score:.2f})"))
    else:
        contributions.append(("Geo-Location Anomaly", loc_contrib, f"Standard geo-location match ({location_risk_score:.2f})"))

    # 7. Velocity 24h
    if velocity_24h > 10:
        vel_contrib = +0.25
        contributions.append(("24-Hour Velocity", vel_contrib, f"Extreme rapid velocity ({velocity_24h} attempts/24h)"))
    elif velocity_24h > 4:
        vel_contrib = +0.10
        contributions.append(("24-Hour Velocity", vel_contrib, f"Elevated velocity ({velocity_24h} attempts/24h)"))
    else:
        vel_contrib = -0.05
        contributions.append(("24-Hour Velocity", vel_contrib, f"Normal user velocity ({velocity_24h} attempt/24h)"))

    # 8. Previous Chargebacks
    cb_contrib = min(previous_chargebacks * 0.15, 0.40)
    if previous_chargebacks > 0:
        contributions.append(("Historical Chargebacks", cb_contrib, f"{previous_chargebacks} prior chargeback record(s) logged"))
    else:
        contributions.append(("Historical Chargebacks", 0.0, "Zero prior chargebacks on record"))

    # 9. Payment Method Risk
    pay_contrib = (payment_method_risk - 0.25) * 0.18
    contributions.append(("Payment Method Risk", pay_contrib, f"Payment instrument risk weighting ({payment_method_risk:.2f})"))

    # Total Score Calculation
    total_raw = base_risk + sum(c[1] for c in contributions)
    risk_score_pct = float(np.clip(total_raw * 100, 1.0, 99.5))

    # Tiers & Recommendations
    if risk_score_pct >= 70.0:
        pred_status = "🚨 DECLINE / HIGH FRAUD RISK"
        risk_badge = "🔴 HIGH RISK TIER (>70%)"
        recommendation_html = """
        <div style="background-color: #450a0a; border-left: 5px solid #ef4444; padding: 12px; border-radius: 6px; color: #fecdd3;">
            <h4 style="margin: 0 0 6px 0; color: #f87171;">🛑 Business Action: DECLINE & ROUTE TO MANUAL REVIEW</h4>
            <p style="margin: 0; font-size: 14px;">High anomaly indicators detected. Block real-time payout or require manual risk analyst review before order fulfillment.</p>
        </div>
        """
    elif risk_score_pct >= 30.0:
        pred_status = "⚠️ STEP-UP VERIFICATION REQUIRED"
        risk_badge = "🟡 MODERATE RISK TIER (30%-70%)"
        recommendation_html = """
        <div style="background-color: #451a03; border-left: 5px solid #f59e0b; padding: 12px; border-radius: 6px; color: #fef3c7;">
            <h4 style="margin: 0 0 6px 0; color: #fbbf24;">🔍 Business Action: CHALLENGE VIA 3D SECURE / OTP</h4>
            <p style="margin: 0; font-size: 14px;">Elevated risk signals present. Route order to 3DS 2.0 or SMS OTP verification before clearing authorization.</p>
        </div>
        """
    else:
        pred_status = "✅ APPROVED / LOW RISK"
        risk_badge = "🟢 LOW RISK TIER (<30%)"
        recommendation_html = """
        <div style="background-color: #052e16; border-left: 5px solid #22c55e; padding: 12px; border-radius: 6px; color: #dcfce7;">
            <h4 style="margin: 0 0 6px 0; color: #4ade80;">⚡ Business Action: INSTANT AUTO-APPROVE</h4>
            <p style="margin: 0; font-size: 14px;">Low-risk parameters confirmed. Clear transaction for immediate instant processing.</p>
        </div>
        """

    # Format Visual XAI Table & Bar Visualization
    sorted_contribs = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)
    
    xai_html = """
    <div style="margin-top: 10px;">
        <h4 style="margin-bottom: 10px; color: #38bdf8;">🔬 Explainable AI (XAI) Feature Attribution Breakdown</h4>
        <table style="width:100%; border-collapse: collapse; text-align: left; font-size: 13px;">
            <thead>
                <tr style="background-color: #1e293b; color: #94a3b8; border-bottom: 2px solid #334155;">
                    <th style="padding: 8px;">Feature Attribute</th>
                    <th style="padding: 8px;">Impact Direction</th>
                    <th style="padding: 8px;">Risk Contribution</th>
                    <th style="padding: 8px;">Audit Explanation</th>
                </tr>
            </thead>
            <tbody>
    """

    for factor, weight, desc in sorted_contribs:
        if weight > 0:
            direction_badge = "<span style='color: #ef4444; font-weight: bold;'>📈 + Risk</span>"
            bar_color = "#ef4444"
            width_pct = min(abs(weight) * 200, 100)
        elif weight < 0:
            direction_badge = "<span style='color: #22c55e; font-weight: bold;'>📉 - Safety</span>"
            bar_color = "#22c55e"
            width_pct = min(abs(weight) * 200, 100)
        else:
            direction_badge = "<span style='color: #94a3b8;'>➖ Neutral</span>"
            bar_color = "#94a3b8"
            width_pct = 2.0

        bar_html = f"<div style='background-color: {bar_color}; width: {width_pct:.0f}%; height: 8px; border-radius: 4px;'></div>"

        xai_html += f"""
        <tr style="border-bottom: 1px solid #334155;">
            <td style="padding: 8px; font-weight: 600;">{factor}</td>
            <td style="padding: 8px;">{direction_badge}</td>
            <td style="padding: 8px;">
                <div style="font-weight: bold; margin-bottom: 3px;">{weight*100:+.1f}%</div>
                {bar_html}
            </td>
            <td style="padding: 8px; color: #cbd5e1;">{desc}</td>
        </tr>
        """

    xai_html += """
            </tbody>
        </table>
        <p style="font-size: 11px; color: #64748b; margin-top: 8px;">*Additive feature attribution computed against baseline system risk of 5.0%.</p>
    </div>
    """

    return pred_status, f"{risk_score_pct:.1f}%", risk_badge, recommendation_html, xai_html


# Custom CSS styling for enterprise appearance
custom_css = """
.gradio-container { background-color: #0f172a; color: #f8fafc; }
h1, h2, h3 { font-family: 'Inter', system-ui, sans-serif; }
.panel-box { background: #1e293b; border-radius: 8px; padding: 15px; }
"""

theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="indigo",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme, css=custom_css, title="Lead.AI Fraud Shield — Explainable Risk Engine") as demo:
    gr.Markdown(
        """
        # 🛡️ Lead.AI Fraud Shield — Explainable Fraud Detection Demo
        ### *Trustworthy AI, Risk Scoring & Explainability for Business Workflows*
        
        **Official Product Showcase:** [Lead.AI Labs](https://www.lead-ai.us) | **Founder:** Arun Kumar Gharami
        
        Adjust the 9 transaction parameters below to evaluate real-time fraud probability and receive an instant **Explainable AI (XAI)** audit breakdown.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Transaction Input Parameters")
            amount = gr.Number(label="Transaction Amount ($)", value=1250.00, precision=2)
            transaction_hour = gr.Slider(label="Transaction Hour (0-23)", minimum=0, maximum=23, step=1, value=3)
            merchant_risk_score = gr.Slider(label="Merchant Category Risk Index (0.0=Safe, 1.0=High)", minimum=0.0, maximum=1.0, step=0.01, value=0.85)
            customer_age_days = gr.Number(label="Customer Account Age (Days)", value=12, precision=0)
            device_trust_score = gr.Slider(label="Device Trust Fingerprint (0.0=Untrusted, 1.0=Verified)", minimum=0.0, maximum=1.0, step=0.01, value=0.15)
            location_risk_score = gr.Slider(label="Geo-Location Anomaly / Proxy Risk (0.0-1.0)", minimum=0.0, maximum=1.0, step=0.01, value=0.88)
            velocity_24h = gr.Slider(label="24-Hour Velocity Attempt Count", minimum=1, maximum=30, step=1, value=14)
            previous_chargebacks = gr.Number(label="Historical Chargebacks Logged", value=2, precision=0)
            payment_method_risk = gr.Slider(label="Payment Method Risk Index (0.0-1.0)", minimum=0.0, maximum=1.0, step=0.01, value=0.80)

            submit_btn = gr.Button("🛡️ Calculate Fraud Risk & XAI Attribution", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 📤 Real-Time Risk Analysis & XAI Audit")
            pred_output = gr.Textbox(label="Prediction Status", interactive=False)
            
            with gr.Row():
                score_output = gr.Textbox(label="Calculated Risk Probability", interactive=False)
                level_output = gr.Textbox(label="Risk Assessment Tier", interactive=False)

            rec_output = gr.HTML(label="Business Action Recommendation")
            xai_output = gr.HTML(label="Explainable AI Breakdown")

    # Interactive Sample Presets
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
        outputs=[pred_output, score_output, level_output, rec_output, xai_output],
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
        outputs=[pred_output, score_output, level_output, rec_output, xai_output]
    )

    gr.Markdown(
        """
        ---
        ### 🌉 The 4-Pillar Lead.AI Ecosystem Bridge
        * 🌐 **Official Business Website:** [www.lead-ai.us](https://www.lead-ai.us) — Enterprise AI solutions, custom risk modeling & consultation
        * 💻 **GitHub Control Center:** [github.com/Arungharami/lead-ai-labs-hf-upgrade](https://github.com/Arungharami/lead-ai-labs-hf-upgrade) — Central engineering code & CLI sync scripts
        * 🤖 **Hugging Face Hub:** [huggingface.co/lead-ai-labs](https://huggingface.co/lead-ai-labs) — Open models, datasets & live Gradio demos
        * 📊 **Kaggle Data Science Hub:** [kaggle.com/arungharami](https://www.kaggle.com/arungharami) — Benchmark kernels, Kaggle datasets & notebook EDA showcase
        
        *Disclaimer: Synthetic benchmark demonstration model for research, education, and prototyping. No real customer banking or financial PII data is stored or processed.*
        """
    )

if __name__ == "__main__":
    demo.launch()
