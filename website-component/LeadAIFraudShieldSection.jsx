import React, { useState } from 'react';

/**
 * Lead.AI Fraud Shield — Enterprise React Product Section
 * Designed for www.lead-ai.us
 * Built by Lead.AI Labs (Arun Kumar Gharami)
 */
export default function LeadAIFraudShieldSection() {
  const [selectedTier, setSelectedTier] = useState('Professional');

  const pricingTiers = [
    {
      name: 'Free Demo',
      price: '$0.00',
      period: 'forever',
      description: 'Public Hugging Face demo, Kaggle benchmark notebook, and open synthetic dataset for self-guided testing.',
      features: [
        'Interactive Gradio Web App Demo',
        'Open SHAP Explainability Attribution',
        'Kaggle EDA & Benchmark Notebook',
        'Synthetic 100+ Record Benchmark CSV'
      ],
      ctaText: 'Try Free Demo',
      ctaLink: 'https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo',
      badge: 'Open Science',
      highlighted: false
    },
    {
      name: 'Starter',
      price: '$299',
      period: 'one-time',
      description: 'Custom risk evaluation report and feature attribution audit on up to 50,000 tabular records.',
      features: [
        '50k Record Tabular Risk Audit',
        'SHAP & LIME Feature Attribution Analysis',
        'False Positive Reduction Insights',
        '60-Min Consultation with Arun Kumar Gharami'
      ],
      ctaText: 'Request Starter Audit',
      ctaLink: 'https://www.lead-ai.us#contact',
      badge: 'Small Business',
      highlighted: false
    },
    {
      name: 'Professional',
      price: '$999',
      period: 'one-time',
      description: 'Custom explainable fraud model trained on your proprietary dataset with private dashboard and API integration.',
      features: [
        'Custom XGBoost / Ensemble Model Training',
        'Calibrated Risk Tiers (Low, Moderate, High)',
        'Private Gradio / Streamlit Web App Interface',
        'Python & FastAPI Integration Code Specs',
        '30-Day Deployment Support'
      ],
      ctaText: 'Get Professional Model',
      ctaLink: 'https://www.lead-ai.us#contact',
      badge: 'Most Popular',
      highlighted: true
    },
    {
      name: 'Business',
      price: '$2,500',
      period: 'project',
      description: 'End-to-end cloud production deployment with real-time API webhooks, automated retraining, and drift monitoring.',
      features: [
        'Multi-Model Pipeline (Fraud + Churn + Risk)',
        'Cloud Deployment (AWS / GCP / Firebase / Docker)',
        'Real-Time Slack & Webhook Risk Alerts',
        'Automated Retraining & Drift Monitoring',
        'Dedicated 60-Day SLA Support'
      ],
      ctaText: 'Deploy Business Pipeline',
      ctaLink: 'https://www.lead-ai.us#contact',
      badge: 'Fintech Ready',
      highlighted: false
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'quote',
      description: 'Full custom enterprise AI architecture, private VPC deployment, SLA guarantees, and ethical AI compliance.',
      features: [
        'On-Premise / Private VPC Zero-Egress Setup',
        'Custom Financial Compliance & Audit Logs',
        '24/7 Dedicated AI Engineer Support',
        'Custom Workflow & ERP/CRM Integration',
        'Full Model Weights Ownership'
      ],
      ctaText: 'Book Enterprise Call',
      ctaLink: 'https://www.lead-ai.us#contact',
      badge: 'Custom Architecture',
      highlighted: false
    }
  ];

  return (
    <section className="bg-slate-950 text-slate-100 py-20 px-4 sm:px-6 lg:px-8 font-sans border-t border-slate-800">
      <div className="max-w-7xl mx-auto">
        
        {/* Brand System Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-4">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            Lead.AI Labs Flagship Product Showcase
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight mb-4">
            Lead.AI Fraud Shield
          </h2>
          <p className="text-lg sm:text-xl text-slate-300 font-medium leading-relaxed">
            Explainable AI Systems for Business Automation, Fraud Detection, and Predictive Intelligence.
          </p>
        </div>

        {/* Problem vs Solution Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {/* Problem Card */}
          <div className="bg-slate-900/90 border border-red-500/20 rounded-xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 rounded-full blur-2xl"></div>
            <div className="text-red-400 text-sm font-bold uppercase tracking-wider mb-2">The Business Challenge</div>
            <h3 className="text-2xl font-bold text-white mb-4">Black-Box ML & Opaque Fraud Decline Rules</h3>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
              Modern payment gateways and e-commerce stores lose billions annually to fraud and false positives. Traditional rule engines miss subtle velocity patterns, while standard "black-box" neural networks fail to explain <span className="text-red-300 font-semibold">why</span> a transaction was flagged—exposing businesses to customer churn and audit compliance risks.
            </p>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-400">
              <li className="flex items-center gap-2">
                <span className="text-red-400">✕</span> High false positive rate turning away legitimate buyers
              </li>
              <li className="flex items-center gap-2">
                <span className="text-red-400">✕</span> Zero transparency for manual risk analyst review queues
              </li>
              <li className="flex items-center gap-2">
                <span className="text-red-400">✕</span> Expensive chargeback fees and unexplainable AI decisions
              </li>
            </ul>
          </div>

          {/* Solution Card */}
          <div className="bg-slate-900/90 border border-cyan-500/30 rounded-xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl"></div>
            <div className="text-cyan-400 text-sm font-bold uppercase tracking-wider mb-2">The Lead.AI Solution</div>
            <h3 className="text-2xl font-bold text-white mb-4">Transparent SHAP XAI & Real-Time Risk Scoring</h3>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
              <strong>Lead.AI Fraud Shield</strong> combines high-precision gradient boosted tabular classification with instantaneous <strong>Explainable AI (SHAP / LIME)</strong> additive feature attributions. Every score is paired with an audit-ready breakdown explaining the exact positive and negative risk factors.
            </p>
            <ul className="space-y-2 text-xs sm:text-sm text-slate-300">
              <li className="flex items-center gap-2">
                <span className="text-cyan-400">✓</span> Instant Risk Probability (0–100%) with calibrated risk tiers
              </li>
              <li className="flex items-center gap-2">
                <span className="text-cyan-400">✓</span> Quantitative feature impact scores (Velocity, Device Trust, Amount)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-cyan-400">✓</span> Actionable business recommendations (Auto-Approve, 3DS OTP, Manual Review)
              </li>
            </ul>
          </div>
        </div>

        {/* Live Interactive Proof & Multi-Platform Badges */}
        <div className="bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border border-slate-800 rounded-2xl p-8 mb-16 shadow-2xl">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-8">
            <div className="space-y-3 text-center lg:text-left">
              <h3 className="text-2xl sm:text-3xl font-bold text-white">Experience Lead.AI Fraud Shield Live</h3>
              <p className="text-slate-300 text-sm sm:text-base max-w-2xl">
                Test real-time fraud probability evaluation, SHAP explainability breakdowns, and automated business recommendations directly on our open Hugging Face Space demo and Kaggle benchmark notebook.
              </p>
            </div>
            
            <div className="flex flex-wrap justify-center gap-4">
              <a
                href="https://huggingface.co/spaces/lead-ai-labs/lead-ai-fraud-shield-demo"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-cyan-500/20 flex items-center gap-2"
              >
                <span>🛡️ Try Live Space Demo</span>
              </a>
              <a
                href="https://github.com/Arungharami/lead-ai-fraud-shield"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm border border-slate-700 transition-all flex items-center gap-2"
              >
                <span>💻 View GitHub Repo</span>
              </a>
              <a
                href="https://www.kaggle.com/code/arungharami/lead-ai-fraud-shield-explainable-fraud-detection-demo"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 rounded-lg bg-sky-950 hover:bg-sky-900 text-sky-300 font-semibold text-sm border border-sky-800 transition-all flex items-center gap-2"
              >
                <span>📊 Kaggle Notebook</span>
              </a>
            </div>
          </div>
        </div>

        {/* Pricing & Service Packages Catalog */}
        <div className="mb-16">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h3 className="text-2xl sm:text-3xl font-bold text-white mb-3">AI Integration & Service Packages</h3>
            <p className="text-slate-400 text-sm sm:text-base">
              Transparent tier pricing designed for startups, growing fintech gateways, e-commerce stores, and enterprise platforms.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {pricingTiers.map((tier) => (
              <div
                key={tier.name}
                className={`rounded-xl p-6 flex flex-col justify-between transition-all ${
                  tier.highlighted
                    ? 'bg-slate-900 border-2 border-cyan-400 shadow-xl shadow-cyan-500/10 scale-105'
                    : 'bg-slate-900/60 border border-slate-800 hover:border-slate-700'
                }`}
              >
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-800 text-cyan-400 border border-slate-700">
                      {tier.badge}
                    </span>
                  </div>
                  <h4 className="text-lg font-bold text-white mb-1">{tier.name}</h4>
                  <div className="mb-3">
                    <span className="text-2xl sm:text-3xl font-extrabold text-white">{tier.price}</span>
                    <span className="text-xs text-slate-400 ml-1">/{tier.period}</span>
                  </div>
                  <p className="text-xs text-slate-300 mb-6 leading-relaxed">{tier.description}</p>
                  
                  <ul className="space-y-2 mb-6">
                    {tier.features.map((feat, idx) => (
                      <li key={idx} className="text-xs text-slate-300 flex items-start gap-1.5">
                        <span className="text-cyan-400 shrink-0">✓</span>
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <a
                  href={tier.ctaLink}
                  target={tier.ctaLink.startsWith('http') ? '_blank' : '_self'}
                  rel="noopener noreferrer"
                  className={`w-full py-2.5 rounded-lg text-xs font-bold text-center transition-all ${
                    tier.highlighted
                      ? 'bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-md shadow-cyan-500/20'
                      : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-700'
                  }`}
                >
                  {tier.ctaText}
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* Founder & Enterprise Credibility Footer */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2 text-center md:text-left">
            <h4 className="text-lg font-bold text-white">Built by Lead.AI Labs Engineering</h4>
            <p className="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
              Lead.AI Labs is founded by <strong>Arun Kumar Gharami</strong>, an AI Engineer & Applied Researcher with a background in Computer Science, Artificial Intelligence, Machine Learning, QA validation, explainable AI, fraud detection, predictive analytics, and deployment-ready AI systems.
            </p>
          </div>
          
          <div className="shrink-0 flex gap-4">
            <a
              href="https://www.lead-ai.us"
              className="px-6 py-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all"
            >
              Book AI Consultation
            </a>
          </div>
        </div>

      </div>
    </section>
  );
}
