
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="MetroHealth TransformX Command Center",
    page_icon="🏥",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_data():
    members = pd.read_csv(DATA_DIR / "members.csv", parse_dates=["enrollment_date"])
    providers = pd.read_csv(DATA_DIR / "providers.csv")
    claims = pd.read_csv(DATA_DIR / "claims.csv", parse_dates=["claim_date"])
    finance = pd.read_csv(DATA_DIR / "finance.csv", parse_dates=["month"])
    cx = pd.read_csv(DATA_DIR / "customer_experience.csv", parse_dates=["month"])
    risk = pd.read_csv(DATA_DIR / "compliance_risk.csv", parse_dates=["month"])
    ai = pd.read_csv(DATA_DIR / "ai_models.csv")
    roadmap = pd.read_csv(DATA_DIR / "transformation_roadmap.csv")
    claims["month"] = claims["claim_date"].dt.to_period("M").dt.to_timestamp()
    return members, providers, claims, finance, cx, risk, ai, roadmap

members, providers, claims, finance, cx, risk, ai, roadmap = load_data()

def money(x):
    if x >= 1_000_000_000:
        return f"₦{x/1_000_000_000:.2f}B"
    if x >= 1_000_000:
        return f"₦{x/1_000_000:.1f}M"
    return f"₦{x:,.0f}"

def page_header(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">MetroHealth TransformX</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def status_badge(label, status):
    color = {"Green": "#15803d", "Amber": "#b45309", "Red": "#b91c1c"}.get(status, "#334155")
    return f"<span style='background:{color}; color:white; padding:4px 10px; border-radius:999px; font-weight:700;'>{label}</span>"

def gauge(title, value, suffix="%", max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix},
        title={"text": title},
        gauge={
            "axis": {"range": [None, max_value]},
            "bar": {"color": "#0f766e"},
            "steps": [
                {"range": [0, 40], "color": "#fee2e2"},
                {"range": [40, 70], "color": "#fef3c7"},
                {"range": [70, 100], "color": "#dcfce7"},
            ],
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
    return fig

st.markdown("""
<style>
    .hero {
        padding: 1.25rem 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #0b1f3a 0%, #0f766e 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
    }
    .hero h1 {
        margin: 0;
        font-size: 2.35rem;
        letter-spacing: -0.04em;
    }
    .hero p {
        margin-top: 0.35rem;
        color: #e0f2fe;
        font-size: 1.05rem;
    }
    .eyebrow {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #99f6e4;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .architecture-box {
        border: 1px solid #dbeafe;
        border-radius: 16px;
        padding: 1rem;
        background: #f8fafc;
        margin-bottom: 0.75rem;
    }
    .architecture-layer {
        padding: 0.8rem;
        border-radius: 12px;
        margin: 0.45rem 0;
        background: white;
        border-left: 6px solid #0f766e;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.06);
    }
    .small-caption {
        color: #64748b;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🏥 MetroHealth TransformX")
st.sidebar.caption("Executive Command Center")
page = st.sidebar.radio(
    "Navigation",
    [
        "CEO Strategic Dashboard",
        "Transformation Strategy",
        "Claims Intelligence",
        "Provider Intelligence",
        "Customer Experience",
        "Financial Intelligence",
        "Compliance & Risk",
        "AI Intelligence",
        "Transformation Roadmap",
        "Enterprise Architecture",
        "Executive AI Copilot"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Synthetic enterprise healthcare data | Digital Health Transformation & Healthcare AI Strategy")

latest_finance = finance.iloc[-1]
latest_cx = cx.iloc[-1]
latest_risk = risk.iloc[-1]

if page == "CEO Strategic Dashboard":
    page_header(
        "CEO Strategic Dashboard",
        "Real-time enterprise performance, transformation progress, and AI-enabled executive intelligence."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Members", f"{len(members):,}")
    c2.metric("Active Providers", f"{len(providers):,}")
    c3.metric("Monthly Revenue", money(latest_finance["revenue"]))
    c4.metric("Digital Adoption", f"{latest_cx['digital_adoption']*100:.1f}%")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Claims Turnaround", f"{claims['processing_days'].mean():.1f} days", "Target <48 hrs")
    c6.metric("Customer Satisfaction", f"{latest_cx['satisfaction_score']:.1f}%")
    c7.metric("NDPR Score", f"{latest_risk['ndpr_score']:.1f}%")
    c8.metric("AI Portfolio Value", money(ai["business_value"].sum()))

    st.subheader("Executive Scorecard")
    score_cols = st.columns(6)
    score_data = [
        ("Governance", "Green"),
        ("Technology", "Green"),
        ("Data", "Green"),
        ("Analytics", "Green"),
        ("AI", "Amber"),
        ("Interoperability", "Amber")
    ]
    for col, (label, status) in zip(score_cols, score_data):
        col.markdown(status_badge(label, status), unsafe_allow_html=True)

    st.subheader("Enterprise Performance Trends")
    monthly_claims = claims.groupby("month").agg(
        claims_volume=("claim_id", "count"),
        claims_cost=("claim_amount", "sum"),
        avg_processing_days=("processing_days", "mean")
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(finance, x="month", y=["revenue", "claims_cost", "operating_cost"], title="Revenue vs Claims & Operating Cost")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.line(cx, x="month", y=["digital_adoption", "retention_rate"], title="Digital Adoption & Retention")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(gauge("Transformation Progress", roadmap["completion_pct"].mean()), use_container_width=True)
    with col4:
        fig = px.line(monthly_claims, x="month", y="avg_processing_days", title="Claims Turnaround Trend")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Transformation Strategy":

    page_header(
        "Digital Health Transformation Strategy",
        "MetroHealth TransformX 3-Year Enterprise Transformation Program"
    )

    st.subheader("Transformation Vision")

    st.success("""
    Become a data-driven, AI-enabled, patient-centered digital health enterprise
    that leverages analytics, interoperability, intelligent automation, and
    executive intelligence to improve outcomes, operational efficiency,
    compliance, and sustainable growth.
    """)

    st.subheader("Strategic Transformation Pillars")

    pillar1, pillar2 = st.columns(2)

    with pillar1:
        st.info("""
        **1. Digital Core Modernization**
        - Claims Platform Modernization
        - Member Management Transformation
        - Provider Portal Enablement
        - Digital Customer Experience
        """)

        st.info("""
        **2. Enterprise Data & Analytics**
        - Enterprise Data Platform
        - Data Governance
        - Master Data Management
        - Executive Analytics
        """)

        st.info("""
        **3. AI & Intelligent Automation**
        - Fraud Detection
        - Churn Prediction
        - Claims Risk Scoring
        - Executive AI Copilot
        """)

    with pillar2:
        st.info("""
        **4. Interoperability & Integration**
        - API Gateway
        - FHIR Integration
        - Provider Connectivity
        - Ecosystem Integration
        """)

        st.info("""
        **5. Governance, Risk & Compliance**
        - IT Governance
        - Data Governance
        - AI Governance
        - Cybersecurity
        """)

        st.info("""
        **6. Workforce & Operating Model**
        - Digital Skills Development
        - Change Management
        - Agile Delivery
        - Product-Centric Teams
        """)

    st.subheader("3-Year Transformation Roadmap")

    y1, y2, y3 = st.columns(3)

    with y1:
        st.success("""
        **Year 1 — Stabilize**
        
        • Governance Foundations
        
        • Enterprise Architecture
        
        • Data Platform
        
        • Digital Core Assessment
        
        • KPI Framework
        """)

    with y2:
        st.warning("""
        **Year 2 — Optimize**
        
        • Analytics Expansion
        
        • Process Automation
        
        • Provider Integration
        
        • Operational Intelligence
        
        • Digital Adoption
        """)

    with y3:
        st.info("""
        **Year 3 — Transform**
        
        • AI at Scale
        
        • Executive AI Copilot
        
        • Predictive Enterprise
        
        • Intelligent Operations
        
        • Continuous Innovation
        """)

    st.subheader("Expected Strategic Outcomes")

    outcome_cols = st.columns(5)

    outcome_cols[0].metric("Claims Processing", "<48 hrs")
    outcome_cols[1].metric("Digital Adoption", "80%+")
    outcome_cols[2].metric("Member Retention", ">90%")
    outcome_cols[3].metric("Compliance", "95%+")
    outcome_cols[4].metric("AI-Enabled Decisions", "Enterprise-Wide")

elif page == "Claims Intelligence":
    page_header("Claims Intelligence Center", "Claims operations, cost intelligence, fraud alerts, and turnaround monitoring.")

    approved = (claims["approval_status"] == "Approved").sum()
    rejected = (claims["approval_status"] == "Rejected").sum()
    fraud = (claims["fraud_flag"] == "Yes").sum()
    high_risk = (claims["risk_score"] >= 75).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Claims", f"{len(claims):,}")
    c2.metric("Approved", f"{approved:,}")
    c3.metric("Rejected", f"{rejected:,}")
    c4.metric("Fraud Alerts", f"{fraud:,}")
    c5.metric("High-Risk Claims", f"{high_risk:,}")

    monthly = claims.groupby("month").agg(
        claims_volume=("claim_id", "count"),
        claims_cost=("claim_amount", "sum"),
        avg_processing_days=("processing_days", "mean"),
        fraud_alerts=("fraud_flag", lambda s: (s == "Yes").sum())
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.line(monthly, x="month", y="claims_volume", title="Claims Volume Trend"), use_container_width=True)
    with col2:
        st.plotly_chart(px.line(monthly, x="month", y="claims_cost", title="Claims Cost Trend"), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        status = claims["approval_status"].value_counts().reset_index()
        status.columns = ["status", "count"]
        st.plotly_chart(px.pie(status, names="status", values="count", title="Claims Status Distribution"), use_container_width=True)
    with col4:
        provider_cost = claims.groupby("provider_id")["claim_amount"].sum().nlargest(15).reset_index()
        st.plotly_chart(px.bar(provider_cost, x="claim_amount", y="provider_id", orientation="h", title="Top 15 Providers by Claims Cost"), use_container_width=True)

elif page == "Provider Intelligence":
    page_header("Provider Intelligence Center", "Provider performance, utilization, reimbursement, and network optimization intelligence.")

    underperforming = (providers["performance_score"] < 60).sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Providers", f"{len(providers):,}")
    c2.metric("Avg Performance", f"{providers['performance_score'].mean():.1f}%")
    c3.metric("Avg Reimbursement", f"{providers['reimbursement_days'].mean():.1f} days")
    c4.metric("Underperforming", f"{underperforming}")

    col1, col2 = st.columns(2)
    with col1:
        top = providers.sort_values("performance_score", ascending=False).head(15)
        st.plotly_chart(px.bar(top, x="performance_score", y="provider_name", orientation="h", title="Top Provider Performance"), use_container_width=True)
    with col2:
        state_counts = providers["state"].value_counts().reset_index()
        state_counts.columns = ["state", "providers"]
        st.plotly_chart(px.bar(state_counts, x="state", y="providers", title="Provider Distribution by State"), use_container_width=True)

    st.dataframe(providers.sort_values("performance_score", ascending=False).head(50), use_container_width=True)

elif page == "Customer Experience":
    page_header("Customer Experience Center", "Member satisfaction, retention, churn risk, complaints, and digital engagement.")

    high_churn = (members["churn_risk"] == "High").sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Satisfaction Score", f"{latest_cx['satisfaction_score']:.1f}%")
    c2.metric("Retention Rate", f"{latest_cx['retention_rate']*100:.1f}%")
    c3.metric("High Churn Risk", f"{high_churn:,}")
    c4.metric("Avg Resolution", f"{latest_cx['avg_resolution_days']:.1f} days")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.line(cx, x="month", y=["satisfaction_score", "nps"], title="Satisfaction & NPS Trend"), use_container_width=True)
    with col2:
        st.plotly_chart(px.line(cx, x="month", y=["complaints", "avg_resolution_days"], title="Complaints & Resolution Trend"), use_container_width=True)

    churn = members["churn_risk"].value_counts().reset_index()
    churn.columns = ["churn_risk", "members"]
    st.plotly_chart(px.pie(churn, names="churn_risk", values="members", title="Member Churn Risk Distribution"), use_container_width=True)

elif page == "Financial Intelligence":
    page_header("Financial Intelligence Center", "Revenue, claims cost, operating cost, profit, ROI, and financial forecasting.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", money(latest_finance["revenue"]))
    c2.metric("Claims Cost", money(latest_finance["claims_cost"]))
    c3.metric("Operating Cost", money(latest_finance["operating_cost"]))
    c4.metric("Profit", money(latest_finance["profit"]))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.line(finance, x="month", y=["revenue", "claims_cost", "operating_cost", "profit"], title="Financial Performance Trend"), use_container_width=True)
    with col2:
        by_region = claims.merge(providers[["provider_id", "state"]], on="provider_id").groupby("state")["claim_amount"].sum().reset_index()
        st.plotly_chart(px.bar(by_region, x="state", y="claim_amount", title="Claims Cost by Provider Region"), use_container_width=True)

    st.dataframe(finance.tail(12), use_container_width=True)

elif page == "Compliance & Risk":
    page_header("Compliance & Risk Center", "NDPR, NHIA, cybersecurity, audit readiness, and enterprise risk monitoring.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("NDPR Score", f"{latest_risk['ndpr_score']:.1f}%")
    c2.metric("NHIA Score", f"{latest_risk['nhia_score']:.1f}%")
    c3.metric("Audit Findings", int(latest_risk["audit_findings"]))
    c4.metric("Security Incidents", int(latest_risk["security_incidents"]))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.line(risk, x="month", y=["ndpr_score", "nhia_score"], title="Compliance Score Trend"), use_container_width=True)
    with col2:
        st.plotly_chart(px.line(risk, x="month", y=["audit_findings", "security_incidents"], title="Audit & Security Events"), use_container_width=True)

    st.dataframe(risk.tail(12), use_container_width=True)

elif page == "AI Intelligence":
    page_header("AI Intelligence Center", "AI portfolio performance, responsible AI metrics, model monitoring, and business value.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AI Models", len(ai))
    c2.metric("Avg Accuracy", f"{ai['accuracy'].mean()*100:.1f}%")
    c3.metric("Avg Explainability", f"{ai['explainability_score'].mean()*100:.1f}%")
    c4.metric("Business Value", money(ai["business_value"].sum()))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(ai, x="model_name", y=["accuracy", "precision", "recall", "f1_score"], barmode="group", title="Model Performance"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(ai, x="model_name", y="business_value", title="Estimated Business Value by AI Use Case"), use_container_width=True)

    st.subheader("AI Governance & Monitoring")
    st.dataframe(ai, use_container_width=True)

elif page == "Transformation Roadmap":
    page_header("Transformation Roadmap", "Portfolio execution, workstream progress, budget utilization, and executive delivery governance.")

    total_budget = roadmap["budget"].sum()
    total_spend = roadmap["spend"].sum()
    avg_completion = roadmap["completion_pct"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Budget", money(total_budget))
    c2.metric("Total Spend", money(total_spend))
    c3.metric("Budget Utilization", f"{total_spend/total_budget*100:.1f}%")
    c4.metric("Avg Completion", f"{avg_completion:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(roadmap, x="completion_pct", y="initiative", color="status", orientation="h", title="Initiative Completion"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(roadmap, x="workstream", y=["budget", "spend"], barmode="group", title="Budget vs Spend by Workstream"), use_container_width=True)

    st.dataframe(roadmap, use_container_width=True)

elif page == "Enterprise Architecture":
    page_header("Enterprise Architecture Blueprint", "CIO-level view of the Intelligent Digital Health Enterprise Architecture.")

    layers = [
        ("6. Executive Intelligence Layer", "Executive Command Center • CEO/CIO/CFO/COO Cockpits • Executive AI Copilot • Real-Time KPIs"),
        ("5. AI & Intelligent Automation Layer", "Fraud Detection • Claims Risk Scoring • Churn Prediction • Provider Intelligence • Population Health Analytics"),
        ("4. Analytics & Business Intelligence Layer", "Operational Analytics • Customer Analytics • Provider Analytics • Financial Analytics • Compliance Analytics"),
        ("3. Enterprise Data Platform Layer", "Data Lake • Data Warehouse • Master Data Management • Metadata Repository • Data Quality Framework"),
        ("2. Integration & Interoperability Layer", "API Gateway • FHIR • HL7 • ICD-10 • SNOMED CT • LOINC • NHIA & Provider Integrations"),
        ("1. Digital Core Systems Layer", "Claims Management • Member Management • Provider Management • CRM • Finance & Billing • Compliance"),
    ]

    for title, description in layers:
        st.info(f"**{title}**\n\n{description}")

    st.subheader("Enterprise Governance Overlay")
    gov_cols = st.columns(5)
    gov_cols[0].info("IT Governance\n\nCOBIT • ITIL")
    gov_cols[1].info("EA Governance\n\nTOGAF")
    gov_cols[2].info("Data Governance\n\nQuality • Stewardship")
    gov_cols[3].info("AI Governance\n\nExplainability • Bias")
    gov_cols[4].info("Cybersecurity\n\nNIST • ISO 27001 • NDPR")

    st.subheader("Strategic Value Outcomes")
    value_cols = st.columns(6)
    outcomes = [
        "Operational Excellence\n\nClaims <48 Hours",
        "Financial Performance\n\nLower Cost Per Claim",
        "Customer Experience\n\n80%+ Digital Adoption",
        "Compliance Excellence\n\nReal-Time Reporting",
        "Executive Intelligence\n\nData-Driven Decisions",
        "Digital Health Enterprise\n\nAI-Enabled Growth"
    ]

    for col, outcome in zip(value_cols, outcomes):
        col.success(outcome)

elif page == "Executive AI Copilot":
    page_header("Executive AI Copilot", "Prototype executive decision support for strategic, operational, financial, and AI questions.")

    question = st.text_input(
        "Ask an executive question",
        placeholder="Example: Why are claims costs increasing?"
    )

    if question:
        q = question.lower()
        monthly_claims = claims.groupby("month").agg(
            claims_cost=("claim_amount", "sum"),
            claims_volume=("claim_id", "count"),
            avg_processing_days=("processing_days", "mean")
        ).reset_index()
        latest_claims = monthly_claims.iloc[-1]
        prior_claims = monthly_claims.iloc[-2]
        cost_change = ((latest_claims["claims_cost"] - prior_claims["claims_cost"]) / prior_claims["claims_cost"]) * 100

        st.subheader("Executive Response")

        if "claim" in q or "cost" in q:
            top_providers = claims.groupby("provider_id")["claim_amount"].sum().nlargest(5).reset_index()
            st.write(f"Claims cost changed by **{cost_change:.1f}%** compared with the previous month.")
            st.write("The most likely drivers are high-cost providers, claim volume changes, service mix, and high-risk claims concentration.")
            st.dataframe(top_providers, use_container_width=True)
            st.success("Recommended actions: review high-cost providers, prioritize high-risk claims, and strengthen fraud detection rules.")
        elif "churn" in q or "member" in q:
            churn = members["churn_risk"].value_counts(normalize=True) * 100
            st.write(f"High churn risk members currently represent **{churn.get('High', 0):.1f}%** of the membership base.")
            st.success("Recommended actions: launch targeted retention campaigns, improve claims transparency, and personalize digital engagement.")
        elif "provider" in q:
            low = providers[providers["performance_score"] < 60].sort_values("performance_score").head(10)
            st.write(f"There are **{len(low)}** providers below the performance threshold.")
            st.dataframe(low, use_container_width=True)
            st.success("Recommended actions: initiate provider performance reviews and prioritize training or contract renegotiation.")
        elif "transformation" in q or "behind" in q:
            behind = roadmap[roadmap["status"].isin(["Red", "Amber"])].sort_values("completion_pct")
            st.write("The following initiatives require executive attention:")
            st.dataframe(behind, use_container_width=True)
            st.success("Recommended actions: resolve dependencies, adjust budget allocation, and escalate red-status initiatives to the Steering Committee.")
        else:
            st.write("I can analyze claims, member churn, provider performance, financial performance, compliance, or transformation progress.")
            st.info("Try asking: Which providers are underperforming? Why are claims costs increasing? Which initiatives are behind schedule?")
