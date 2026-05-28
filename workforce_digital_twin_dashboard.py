"""
Workforce Digital Twin Dashboard — SAP SuccessFactors
Prototype for MBA Industry Project (Alex Chen)
SAP-styled UI replicating the look and feel of SAP Fiori / SuccessFactors
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json

# ─────────────────────────────────────────────
# SAP FIORI DESIGN TOKENS
# ─────────────────────────────────────────────
SAP_BLUE       = "#0070F2"
SAP_DARK_BLUE  = "#003575"
SAP_TEAL       = "#1B6CA8"
SAP_LIGHT_BG   = "#F5F6F7"
SAP_WHITE      = "#FFFFFF"
SAP_BORDER     = "#D9D9D9"
SAP_TEXT_DARK  = "#1A1A1A"
SAP_TEXT_MUTED = "#6A6D70"
SAP_SUCCESS    = "#107E3E"
SAP_WARNING    = "#E9730C"
SAP_ERROR      = "#BB0000"
SAP_HIGHLIGHT  = "#E0EFFF"

st.set_page_config(
    page_title="SAP | Workforce Digital Twin",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — SAP FIORI LOOK & FEEL
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', '72', Arial, sans-serif;
    background-color: #F5F6F7;
    color: #1A1A1A;
  }

  /* ── SAP Shell Bar ── */
  .sap-shell-bar {
    background: linear-gradient(135deg, #003575 0%, #0057A8 60%, #0070F2 100%);
    padding: 0 24px;
    height: 48px;
    display: flex;
    align-items: center;
    gap: 16px;
    border-bottom: 3px solid #005BB7;
    margin-bottom: 0;
  }
  .sap-logo {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 1px;
  }
  .sap-app-title {
    font-size: 14px;
    color: #BDD7FF;
    font-weight: 400;
    margin-left: 12px;
    padding-left: 12px;
    border-left: 1px solid rgba(255,255,255,0.3);
  }

  /* ── Cards ── */
  .sap-card {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .sap-card-header {
    font-size: 16px;
    font-weight: 600;
    color: #003575;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #0070F2;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ── KPI Tiles ── */
  .kpi-tile {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border-top: 3px solid #0070F2;
  }
  .kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: #003575;
    line-height: 1.1;
  }
  .kpi-label {
    font-size: 12px;
    color: #6A6D70;
    margin-top: 4px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .kpi-delta-pos { color: #107E3E; font-size: 12px; font-weight: 600; }
  .kpi-delta-neg { color: #BB0000; font-size: 12px; font-weight: 600; }

  /* ── Status Badges ── */
  .badge-hot    { background:#FFEEEE; color:#BB0000; border:1px solid #FFCCCC; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600; }
  .badge-warm   { background:#FFF4E5; color:#E9730C; border:1px solid #FFD9A8; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600; }
  .badge-cold   { background:#EAF4FF; color:#0070F2; border:1px solid #B8D9FF; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600; }
  .badge-sold   { background:#EDFFF3; color:#107E3E; border:1px solid #A5DDB8; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600; }
  .badge-at-risk{ background:#FFF8E1; color:#916E00; border:1px solid #F5D87A; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600; }

  /* ── Scenario Tabs ── */
  .scenario-header {
    background: linear-gradient(90deg, #0057A8 0%, #0070F2 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    font-size: 15px;
  }

  /* ── Progress Bar ── */
  .progress-bar-outer {
    background: #E8E8E8;
    border-radius: 6px;
    height: 10px;
    width: 100%;
    margin-top: 4px;
  }
  .progress-bar-inner {
    background: linear-gradient(90deg, #0057A8, #0070F2);
    border-radius: 6px;
    height: 10px;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E0E0E0;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stSlider label {
    color: #003575;
    font-weight: 500;
    font-size: 13px;
  }

  /* ── Streamlit overrides ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #F0F4FF;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #555;
    border-radius: 6px;
    font-weight: 500;
    font-size: 13px;
  }
  .stTabs [aria-selected="true"] {
    background: #0070F2 !important;
    color: white !important;
  }
  .stMetric { background: transparent; }
  div[data-testid="stMetricValue"] { font-size: 28px; color: #003575; font-weight: 700; }
  div[data-testid="stMetricLabel"] { color: #6A6D70; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
  .stAlert { border-radius: 6px; }

  /* ── Dataframe ── */
  .stDataFrame { border-radius: 8px; overflow: hidden; }
  thead tr th { background-color: #003575 !important; color: white !important; }

  /* ── Buttons ── */
  .stButton > button {
    background: #0070F2;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    padding: 8px 20px;
    font-size: 14px;
    transition: background 0.2s;
  }
  .stButton > button:hover { background: #0057A8; }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SHELL BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="sap-shell-bar">
  <span class="sap-logo">SAP</span>
  <span class="sap-app-title">SuccessFactors · Workforce Digital Twin</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SYNTHETIC DATA — WORKFORCE & PROJECTS
# ─────────────────────────────────────────────
np.random.seed(42)

EMPLOYEES = [
    {"id":"EMP001","name":"Ana Müller","area":"Cloud ERP","role":"Senior Consultant","seniority":"Senior","cost_day":850,"skills":["SAP S/4HANA","Fiori","ABAP"],"allocation_pct":100,"available_from":"2025-09-01","location":"DE"},
    {"id":"EMP002","name":"James Okafor","area":"HR Tech","role":"HCM Architect","seniority":"Lead","cost_day":1100,"skills":["SuccessFactors","HCM","Python"],"allocation_pct":80,"available_from":"2025-07-15","location":"UK"},
    {"id":"EMP003","name":"Sofia Reyes","area":"Data & AI","role":"Data Scientist","seniority":"Mid","cost_day":700,"skills":["ML","Python","BTP"],"allocation_pct":60,"available_from":"2025-06-30","location":"ES"},
    {"id":"EMP004","name":"Tom Lindqvist","area":"Supply Chain","role":"SCM Consultant","seniority":"Senior","cost_day":820,"skills":["SAP IBP","APO","EWM"],"allocation_pct":100,"available_from":"2025-10-01","location":"SE"},
    {"id":"EMP005","name":"Priya Sharma","area":"Cloud ERP","role":"FICO Consultant","seniority":"Mid","cost_day":680,"skills":["FI","CO","RAP"],"allocation_pct":40,"available_from":"2025-06-15","location":"IN"},
    {"id":"EMP006","name":"Carlos Pinto","area":"Data & AI","role":"ML Engineer","seniority":"Senior","cost_day":900,"skills":["TensorFlow","BTP AI","Python"],"allocation_pct":100,"available_from":"2025-11-01","location":"BR"},
    {"id":"EMP007","name":"Lena Hoffman","area":"HR Tech","role":"SF Consultant","seniority":"Junior","cost_day":480,"skills":["SuccessFactors","Recruiting","LMS"],"allocation_pct":20,"available_from":"2025-06-10","location":"DE"},
    {"id":"EMP008","name":"Marcus Webb","area":"Cloud ERP","role":"Basis Admin","seniority":"Mid","cost_day":620,"skills":["Basis","HANA","BTP"],"allocation_pct":100,"available_from":"2025-08-01","location":"US"},
    {"id":"EMP009","name":"Yuki Tanaka","area":"Supply Chain","role":"SCM Lead","seniority":"Lead","cost_day":1050,"skills":["SAP TM","EWM","ARIBA"],"allocation_pct":80,"available_from":"2025-09-15","location":"JP"},
    {"id":"EMP010","name":"Rachel Kim","area":"Data & AI","role":"BI Analyst","seniority":"Senior","cost_day":760,"skills":["SAC","BW/4","Python"],"allocation_pct":60,"available_from":"2025-07-01","location":"KR"},
]

PROJECTS = [
    {"id":"PRJ001","name":"Global S/4HANA Migration – RetailCo","client":"RetailCo","status":"Sold","pipeline_warmth":"Sold","start":"2025-07-01","end":"2026-03-31","value":4200000,"required_skills":["SAP S/4HANA","ABAP","Fiori"],"headcount_needed":4,"allocated":["EMP001","EMP008"],"industry":"Retail"},
    {"id":"PRJ002","name":"SuccessFactors HCM Rollout – PharmaCo","client":"PharmaCo","status":"Hot","pipeline_warmth":"Hot","start":"2025-08-01","end":"2025-12-31","value":1800000,"required_skills":["SuccessFactors","HCM","LMS"],"headcount_needed":3,"allocated":["EMP002","EMP007"],"industry":"Pharma"},
    {"id":"PRJ003","name":"BTP AI Platform – FinTech","client":"FinTechGlobal","status":"Hot","pipeline_warmth":"Hot","start":"2025-09-01","end":"2026-06-30","value":2900000,"required_skills":["BTP AI","ML","Python"],"headcount_needed":3,"allocated":["EMP003"],"industry":"Financial Services"},
    {"id":"PRJ004","name":"Supply Chain Optimisation – AutoCo","client":"AutoCo","status":"Warm","pipeline_warmth":"Warm","start":"2025-10-01","end":"2026-04-30","value":3400000,"required_skills":["SAP IBP","APO","EWM"],"headcount_needed":4,"allocated":["EMP004","EMP009"],"industry":"Automotive"},
    {"id":"PRJ005","name":"Finance Transformation – EnergyGroup","client":"EnergyGroup","status":"Cold","pipeline_warmth":"Cold","start":"2026-01-01","end":"2026-08-31","value":2100000,"required_skills":["FI","CO","RAP"],"headcount_needed":2,"allocated":[],"industry":"Energy"},
    {"id":"PRJ006","name":"SAC Analytics Rollout – InsureCo","client":"InsureCo","status":"Warm","pipeline_warmth":"Warm","start":"2025-11-01","end":"2026-02-28","value":980000,"required_skills":["SAC","BW/4","Python"],"headcount_needed":2,"allocated":[],"industry":"Insurance"},
]

df_emp = pd.DataFrame(EMPLOYEES)
df_proj = pd.DataFrame(PROJECTS)

# ─────────────────────────────────────────────
# SIDEBAR — CONTROLS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='background:#003575;color:white;padding:14px 16px;border-radius:8px;margin-bottom:16px;'>
      <div style='font-size:13px;font-weight:700;letter-spacing:1px;'>🔷 DIGITAL TWIN</div>
      <div style='font-size:11px;color:#99BBDD;margin-top:2px;'>Simulation Control Panel</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**📅 Planning Horizon**")
    horizon = st.slider("Months ahead", 1, 12, 6)

    st.markdown("**🏗️ Pipeline Filter**")
    warmth_filter = st.multiselect(
        "Project warmth",
        ["Sold","Hot","Warm","Cold"],
        default=["Sold","Hot","Warm"]
    )

    st.markdown("**💼 Business Unit**")
    unit_filter = st.selectbox(
        "Select unit",
        ["All Units","Cloud ERP","HR Tech","Data & AI","Supply Chain"]
    )

    st.divider()
    st.markdown("**🤖 AI Simulation Settings**")
    confidence = st.slider("Forecast confidence %", 60, 99, 85)
    attrition_rate = st.slider("Assumed attrition rate %", 5, 25, 12)
    growth_rate = st.slider("Business growth rate %", 0, 30, 15)

    st.divider()
    st.markdown("<div style='font-size:11px;color:#999;'>SAP SuccessFactors · BTP AI Foundation<br>Workforce Digital Twin v1.0-proto<br>© 2025 SAP SE</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Overview",
    "👥  Workforce",
    "📁  Project Pipeline",
    "🔮  Scenario Simulation",
    "🤖  AI Insights"
])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    st.markdown("### Workforce Intelligence Dashboard")
    st.caption(f"Real-time view · Planning horizon: **{horizon} months** · Forecast confidence: **{confidence}%**")

    # KPIs
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1:
        st.markdown("""<div class="kpi-tile"><div class="kpi-value">10</div>
        <div class="kpi-label">Total Employees</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="kpi-tile"><div class="kpi-value" style="color:#107E3E;">82%</div>
        <div class="kpi-label">Avg. Utilisation</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="kpi-tile"><div class="kpi-value">6</div>
        <div class="kpi-label">Active Projects</div></div>""", unsafe_allow_html=True)
    with c4:
        pipeline_val = df_proj[df_proj['pipeline_warmth'].isin(warmth_filter)]['value'].sum()
        st.markdown(f"""<div class="kpi-tile"><div class="kpi-value">€{pipeline_val/1e6:.1f}M</div>
        <div class="kpi-label">Pipeline Value</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown("""<div class="kpi-tile"><div class="kpi-value" style="color:#E9730C;">3</div>
        <div class="kpi-label">Skill Gaps</div></div>""", unsafe_allow_html=True)
    with c6:
        st.markdown("""<div class="kpi-tile"><div class="kpi-value" style="color:#BB0000;">2</div>
        <div class="kpi-label">At-Risk Allocs</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3,2])

    with col_left:
        st.markdown('<div class="sap-card"><div class="sap-card-header">📈 Workforce Demand vs Supply Forecast</div>', unsafe_allow_html=True)
        months = [(datetime.now() + timedelta(days=30*i)).strftime("%b %Y") for i in range(horizon)]
        demand = [8, 10, 12, 13, 14, 15, 16, 17, 18, 18, 19, 20][:horizon]
        supply = [10, 10, 9, 9, 8, 8, 8, 9, 9, 10, 10, 11][:horizon]
        gap    = [max(0, d-s) for d,s in zip(demand,supply)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=demand, name="Projected Demand",
            line=dict(color="#0070F2", width=3), fill='tozeroy',
            fillcolor="rgba(0,112,242,0.08)"))
        fig.add_trace(go.Scatter(x=months, y=supply, name="Available Supply",
            line=dict(color="#107E3E", width=3, dash='dash')))
        fig.add_trace(go.Bar(x=months, y=gap, name="Headcount Gap",
            marker_color="#BB0000", opacity=0.6, yaxis='y'))
        fig.update_layout(
            height=280, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=0,r=0,t=10,b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            yaxis=dict(title="Headcount", gridcolor="#F0F0F0"),
            font=dict(family="Inter", size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="sap-card"><div class="sap-card-header">🎯 Utilisation by Business Unit</div>', unsafe_allow_html=True)
        units = ["Cloud ERP","HR Tech","Data & AI","Supply Chain"]
        util  = [88, 75, 72, 95]
        colors = ["#0070F2" if u >= 80 else "#E9730C" if u >= 70 else "#BB0000" for u in util]
        fig2 = go.Figure(go.Bar(
            x=util, y=units, orientation='h',
            marker_color=colors,
            text=[f"{u}%" for u in util],
            textposition='outside'
        ))
        fig2.add_vline(x=80, line_dash="dash", line_color="#999", annotation_text="Target 80%")
        fig2.update_layout(
            height=280, plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=0,r=20,t=10,b=0),
            xaxis=dict(range=[0,110], title="Utilisation %"),
            font=dict(family="Inter", size=12)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Alerts
    st.markdown("#### ⚠️ AI-Generated Alerts")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.warning("**Supply Chain** will face a headcount gap in Month 4–6. 2 open roles needed (SCM expertise).")
    with col_b:
        st.error("**EMP004 (Tom Lindqvist)** has approved leave overlapping PRJ004 start date. Reallocation needed.")
    with col_c:
        st.info("**3 employees** show <40% allocation next quarter. Consider redeployment or L&D assignments.")


# ══════════════════════════════════════════════
# TAB 2 — WORKFORCE
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### Employee Roster & Availability")

    search = st.text_input("🔍 Search by name, skill, or area", placeholder="e.g. SuccessFactors, Senior, DE...")

    # Build display dataframe
    df_display = df_emp.copy()
    if search:
        mask = df_display.apply(lambda r: search.lower() in str(r.values).lower(), axis=1)
        df_display = df_display[mask]

    for _, emp in df_display.iterrows():
        alloc = emp['allocation_pct']
        alloc_color = "#107E3E" if alloc >= 80 else "#E9730C" if alloc >= 40 else "#BB0000"
        skills_html = " ".join([f"<span style='background:#EAF4FF;color:#0070F2;border:1px solid #B8D9FF;border-radius:10px;padding:1px 8px;font-size:11px;font-weight:600;margin:1px;'>{s}</span>" for s in emp['skills']])
        avail_date = emp['available_from']

        with st.expander(f"👤  {emp['name']}  ·  {emp['role']}  ·  {emp['area']}  ·  {emp['location']}", expanded=False):
            c1,c2,c3,c4 = st.columns([2,1,1,2])
            with c1:
                st.markdown(f"**Seniority:** {emp['seniority']}<br>**Cost:** €{emp['cost_day']:,}/day", unsafe_allow_html=True)
                st.markdown(f"**Skills:**<br>{skills_html}", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**Current Allocation**")
                st.markdown(f"<div style='font-size:28px;font-weight:700;color:{alloc_color};'>{alloc}%</div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"**Available From**<br><div style='font-size:16px;font-weight:600;color:#003575;'>{avail_date}</div>", unsafe_allow_html=True)
            with c4:
                # Allocation bar
                months_mini = [(datetime.now() + timedelta(days=30*i)).strftime("%b") for i in range(6)]
                alloc_data  = [min(100, alloc + random.randint(-10,10)) for _ in range(6)]
                fig_mini = go.Figure(go.Bar(
                    x=months_mini, y=alloc_data,
                    marker_color=["#0070F2" if a>=80 else "#E9730C" if a>=40 else "#BB0000" for a in alloc_data],
                    showlegend=False
                ))
                fig_mini.add_hline(y=80, line_dash="dot", line_color="#999")
                fig_mini.update_layout(
                    height=120, margin=dict(l=0,r=0,t=0,b=0),
                    plot_bgcolor="white", paper_bgcolor="white",
                    yaxis=dict(range=[0,110], showgrid=False, title=None),
                    xaxis=dict(showgrid=False),
                    font=dict(size=10)
                )
                st.plotly_chart(fig_mini, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — PROJECT PIPELINE
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### Project Pipeline & Staffing")

    df_proj_filtered = df_proj[df_proj['pipeline_warmth'].isin(warmth_filter)]

    WARMTH_BADGE = {
        "Sold":  '<span class="badge-sold">SOLD</span>',
        "Hot":   '<span class="badge-hot">HOT</span>',
        "Warm":  '<span class="badge-warm">WARM</span>',
        "Cold":  '<span class="badge-cold">COLD</span>',
    }

    for _, proj in df_proj_filtered.iterrows():
        allocated_names = [e['name'] for e in EMPLOYEES if e['id'] in proj['allocated']]
        gap = proj['headcount_needed'] - len(proj['allocated'])
        gap_color = "#BB0000" if gap > 0 else "#107E3E"

        with st.expander(f"📁  {proj['name']}  ·  {proj['industry']}", expanded=proj['pipeline_warmth']=="Sold"):
            st.markdown(WARMTH_BADGE.get(proj['pipeline_warmth'],''), unsafe_allow_html=True)
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            with c1:
                st.markdown(f"**Client:** {proj['client']}<br>**Industry:** {proj['industry']}<br>**Required Skills:** {', '.join(proj['required_skills'])}", unsafe_allow_html=True)
                if allocated_names:
                    st.markdown(f"**Allocated:** {', '.join(allocated_names)}")
                else:
                    st.markdown("**Allocated:** *None yet*")
            with c2:
                st.markdown(f"**Value**<br><div style='font-size:22px;font-weight:700;color:#003575;'>€{proj['value']/1e6:.1f}M</div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"**Headcount Gap**<br><div style='font-size:22px;font-weight:700;color:{gap_color};'>{gap}</div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"**Start:** {proj['start']}<br>**End:** {proj['end']}")

            # Staffing recommendation
            if gap > 0:
                st.warning(f"⚡ AI Recommendation: {gap} open position(s) for this project. Skills needed: {', '.join(proj['required_skills'])}. Check internal talent pool before external hiring.")

    st.divider()
    st.markdown("#### 📊 Pipeline Gantt View")
    fig_gantt = px.timeline(
        df_proj, x_start="start", x_end="end", y="name", color="pipeline_warmth",
        color_discrete_map={"Sold":"#107E3E","Hot":"#BB0000","Warm":"#E9730C","Cold":"#0070F2"},
        hover_data=["client","value","headcount_needed"],
        title=""
    )
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(
        height=320, plot_bgcolor="white", paper_bgcolor="white",
        legend_title="Pipeline Status",
        font=dict(family="Inter", size=12),
        margin=dict(l=0,r=0,t=10,b=0)
    )
    st.plotly_chart(fig_gantt, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 4 — SCENARIO SIMULATION (DIGITAL TWIN)
# ══════════════════════════════════════════════
with tab4:
    st.markdown("### 🔮 Workforce Digital Twin — Scenario Simulation")
    st.info("This is the core Digital Twin feature. Create sandbox scenarios to simulate workforce decisions before executing them in the real system.")

    scenario_choice = st.radio(
        "**Select a pre-built scenario or create custom:**",
        ["📈 Scenario A: Rapid Pipeline Growth (+30%)",
         "🔄 Scenario B: Internal Mobility vs. External Hiring",
         "🤖 Scenario C: Automation Impact on Finance & HR Roles"],
        horizontal=True
    )

    st.divider()

    # ── SCENARIO A ──────────────────────────────
    if "Scenario A" in scenario_choice:
        st.markdown('<div class="scenario-header">📈 Scenario A — Rapid Pipeline Growth (+30%)</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sap-card">
        <b>Simulation Setup:</b> SAP wins 30% more projects than forecast over the next 6 months, 
        particularly in Cloud ERP and Supply Chain. What is the headcount impact? Can we staff from 
        internal talent? What is the cost delta?
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3,2])
        with col1:
            months = [(datetime.now() + timedelta(days=30*i)).strftime("%b %Y") for i in range(horizon)]
            baseline_demand = [8,10,12,13,14,15][:horizon]
            scenario_demand = [round(d*1.3) for d in baseline_demand]
            supply           = [10,10,9,9,8,8][:horizon]

            fig_a = go.Figure()
            fig_a.add_trace(go.Scatter(x=months,y=baseline_demand,name="Baseline Demand",
                line=dict(color="#999",width=2,dash='dot')))
            fig_a.add_trace(go.Scatter(x=months,y=scenario_demand,name="Scenario A Demand",
                line=dict(color="#0070F2",width=3),fill='tozeroy',fillcolor="rgba(0,112,242,0.08)"))
            fig_a.add_trace(go.Scatter(x=months,y=supply,name="Available Supply",
                line=dict(color="#107E3E",width=2,dash='dash')))
            fig_a.update_layout(height=280,plot_bgcolor="white",paper_bgcolor="white",
                margin=dict(l=0,r=0,t=10,b=0),legend=dict(orientation="h",yanchor="bottom",y=1.02),
                yaxis=dict(title="FTEs",gridcolor="#F0F0F0"),font=dict(family="Inter",size=12))
            st.plotly_chart(fig_a, use_container_width=True)

        with col2:
            st.markdown("#### Simulation Output")
            st.metric("Additional FTEs Required", "+6", delta="vs baseline +0")
            st.metric("Internal Supply Available", "2", delta="4 to hire externally")
            est_hire_cost = 4 * 75000
            st.metric("Estimated Hiring Cost", f"€{est_hire_cost:,}", delta="~€75K/hire")
            ramp_weeks = 12
            st.metric("Ramp-up Time Risk", f"{ramp_weeks} weeks", delta="Time-to-productivity")

        st.markdown("#### 🔑 AI Decision Recommendations")
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        with rec_col1:
            st.markdown("""<div class="sap-card">
            <b>🎯 Redeploy First</b><br>
            EMP005, EMP007, EMP010 have <60% allocation. 
            Upskill for Cloud ERP to close 2 of 6 gaps internally.
            Cost saving vs external hire: <b>~€150K</b>.
            </div>""", unsafe_allow_html=True)
        with rec_col2:
            st.markdown("""<div class="sap-card">
            <b>🤝 Partner Network</b><br>
            For peak periods, engage SAP Partner ecosystem 
            (staff augmentation) for 2 positions. Reduces 
            permanent headcount risk by <b>33%</b>.
            </div>""", unsafe_allow_html=True)
        with rec_col3:
            st.markdown("""<div class="sap-card">
            <b>📋 Talent Pipeline</b><br>
            Activate university partnerships (3 SAP Academy 
            graduates Q3). Long lead-time: initiate now. 
            Cost/FTE vs market: <b>-40%</b>.
            </div>""", unsafe_allow_html=True)

    # ── SCENARIO B ──────────────────────────────
    elif "Scenario B" in scenario_choice:
        st.markdown('<div class="scenario-header">🔄 Scenario B — Internal Mobility vs. External Hiring</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sap-card">
        <b>Simulation Setup:</b> PRJ003 (BTP AI Platform) and PRJ002 (SF HCM) have open positions.
        Compare cost, time, and risk of: (A) retraining existing employees vs (B) external hiring.
        </div>
        """, unsafe_allow_html=True)

        # Comparison table
        comparison_data = {
            "Factor": ["Time to Productivity","Total Cost (Year 1)","Retention Risk","Cultural Fit","Knowledge Continuity","Morale Impact"],
            "🔄 Internal Mobility (Reskill)": ["8-10 weeks","€18,000 (training)","Low","High","High","Positive"],
            "🧑‍💼 External Hiring":          ["12-20 weeks","€75,000-120,000","Medium-High","Medium","Low","Neutral"],
        }
        df_comp = pd.DataFrame(comparison_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            # Cost comparison bar chart
            categories = ["Training Cost","Recruitment Fee","Onboarding","Lost Productivity","Year 1 Total"]
            internal = [18000, 0, 5000, 12000, 35000]
            external = [0, 45000, 8000, 30000, 83000]
            fig_b = go.Figure(data=[
                go.Bar(name='Internal Mobility', x=categories, y=internal, marker_color="#107E3E"),
                go.Bar(name='External Hiring',   x=categories, y=external, marker_color="#0070F2"),
            ])
            fig_b.update_layout(barmode='group',height=280,plot_bgcolor="white",paper_bgcolor="white",
                margin=dict(l=0,r=0,t=10,b=0),yaxis=dict(title="Cost (€)",gridcolor="#F0F0F0"),
                legend=dict(orientation="h",yanchor="bottom",y=1.02),font=dict(family="Inter",size=12))
            st.plotly_chart(fig_b, use_container_width=True)
        with col_b2:
            st.markdown("#### Simulation Verdict")
            st.metric("Cost Saving (Internal vs External)", "€48,000/hire")
            st.metric("Time Advantage (External)", "+6-10 weeks faster")
            st.metric("Recommended for PRJ003", "Internal Mobility", delta="EMP003 → upskill to BTP AI")
            st.metric("Recommended for PRJ002 (urgent)", "External Hire", delta="Start date in 4 weeks")
            st.success("**AI Verdict:** Hybrid approach optimal. Reskill 1 internal employee for non-urgent role; hire externally for immediate delivery need.")

    # ── SCENARIO C ──────────────────────────────
    elif "Scenario C" in scenario_choice:
        st.markdown('<div class="scenario-header">🤖 Scenario C — Automation Impact on Finance & HR Roles</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sap-card">
        <b>Simulation Setup:</b> SAP deploys Joule AI agents across Finance and HR back-office operations.
        30% automation of routine tasks (data entry, report generation, payroll processing).
        Simulate workforce impact over 18 months: roles affected, reskilling needs, cost delta.
        </div>
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns([3,2])
        with col_c1:
            timeline = ["M1","M3","M6","M9","M12","M18"]
            roles_automated_pct = [5, 12, 20, 26, 30, 35]
            reskilled_pct       = [2, 6,  12, 20, 28, 34]
            redeployed_pct      = [1, 4,  8,  14, 20, 28]

            fig_c = go.Figure()
            fig_c.add_trace(go.Scatter(x=timeline,y=roles_automated_pct,name="Tasks Automated %",
                line=dict(color="#BB0000",width=3),fill='tozeroy',fillcolor="rgba(187,0,0,0.06)"))
            fig_c.add_trace(go.Scatter(x=timeline,y=reskilled_pct,name="Employees Reskilled %",
                line=dict(color="#0070F2",width=3)))
            fig_c.add_trace(go.Scatter(x=timeline,y=redeployed_pct,name="Employees Redeployed %",
                line=dict(color="#107E3E",width=3,dash='dash')))
            fig_c.update_layout(height=280,plot_bgcolor="white",paper_bgcolor="white",
                margin=dict(l=0,r=0,t=10,b=0),legend=dict(orientation="h",yanchor="bottom",y=1.02),
                yaxis=dict(title="% of workforce",gridcolor="#F0F0F0"),font=dict(family="Inter",size=12))
            st.plotly_chart(fig_c, use_container_width=True)

        with col_c2:
            st.markdown("#### 18-Month Impact Model")
            st.metric("Roles Partially Automated", "3 of 10", delta="30% task reduction")
            st.metric("Reskilling Investment Needed", "€54,000", delta="€18K/person × 3")
            cost_saving = 3 * 850 * 220 * 0.30
            st.metric("Annual Cost Efficiency Gained", f"€{cost_saving:,.0f}", delta="from automation")
            st.metric("Net ROI (Year 1)", f"€{cost_saving-54000:,.0f}", delta="positive after reskilling")

        st.markdown("#### Role-Level Automation Impact")
        impact_data = {
            "Role":["FICO Consultant","HR Ops Specialist","BI Analyst","Basis Admin","SCM Consultant"],
            "Tasks Automated":["Recurring journal entries, VAT reports","Payroll processing, Leave mgmt","Standard reporting, Data pulls","Routine patches, Monitoring","Order confirmations, Inventory alerts"],
            "Automation %":[35,40,25,20,15],
            "AI Recommendation":["Reskill → AI-FI oversight","Reskill → People Analytics","Expand → AI insights tuning","Expand → BTP DevOps","Stable — strategic value"],
            "Priority":["High","High","Medium","Medium","Low"]
        }
        df_impact = pd.DataFrame(impact_data)
        st.dataframe(df_impact, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 5 — AI INSIGHTS (Joule-style)
# ══════════════════════════════════════════════
with tab5:
    st.markdown("### 🤖 Joule AI — Workforce Intelligence")
    st.info("Powered by SAP Business AI (BTP AI Foundation). This simulates how Joule would surface workforce insights within SuccessFactors.")

    # Simulate Joule chat
    st.markdown('<div class="sap-card"><div class="sap-card-header">💬 Ask Joule</div>', unsafe_allow_html=True)

    quick_prompts = st.columns(4)
    with quick_prompts[0]:
        if st.button("Who can staff PRJ003?"):
            st.session_state['joule_q'] = "Who can staff PRJ003?"
    with quick_prompts[1]:
        if st.button("Show under-utilised employees"):
            st.session_state['joule_q'] = "Show under-utilised employees"
    with quick_prompts[2]:
        if st.button("Forecast Q3 headcount gap"):
            st.session_state['joule_q'] = "Forecast Q3 headcount gap"
    with quick_prompts[3]:
        if st.button("What is our automation readiness?"):
            st.session_state['joule_q'] = "What is our automation readiness?"

    user_q = st.text_input("Or type your question...", value=st.session_state.get('joule_q',''), placeholder="e.g. Who is available in August with BTP skills?")

    JOULE_RESPONSES = {
        "Who can staff PRJ003?": """
**Joule Analysis — PRJ003: BTP AI Platform (FinTechGlobal)**

Required Skills: BTP AI, ML, Python · Headcount Needed: 3 · Start: Sep 2025

**Best Matches:**
| Employee | Match Score | Availability | Gap |
|---|---|---|---|
| Sofia Reyes (EMP003) | ★★★★★ 96% | 60% allocated — has capacity | None |
| Carlos Pinto (EMP006) | ★★★★☆ 82% | 100% allocated until Nov | Timing conflict |
| Rachel Kim (EMP010) | ★★★☆☆ 71% | 60% allocated | BTP AI upskill needed (4 wks) |

**Recommendation:** Assign EMP003 immediately. Initiate upskill plan for EMP010 now (4-week ramp). EMP006 available Nov 1 — negotiate project start or use external resource for M1-M2.
""",
        "Show under-utilised employees": """
**Joule Analysis — Under-Utilised Employees (< 60% allocation)**

| Employee | Current Allocation | Available From | Recommended Action |
|---|---|---|---|
| Sofia Reyes (EMP003) | 60% | Jun 30 | Assign to PRJ003 immediately |
| Priya Sharma (EMP005) | 40% | Jun 15 | L&D: FICO + RAP deep dive; target PRJ005 |
| Lena Hoffman (EMP007) | 20% | Jun 10 | Internal project support; SF certification path |

**Cost of Under-utilisation:** ~€47,600/month at current salary levels.
**Recommendation:** Activate internal mobility + L&D programme immediately. Target 80%+ utilisation within 8 weeks.
""",
        "Forecast Q3 headcount gap": """
**Joule Forecast — Q3 2025 Headcount Analysis (Jul–Sep)**

Confidence Level: 85% · Model: ML demand forecasting on pipeline warmth + historical win rates

**Projected Gap by Unit:**
- Cloud ERP: **+2 FTEs** needed (PRJ001 scaling + new opportunity probability 72%)
- Data & AI: **+1 FTE** needed (PRJ003 requires 3, only 1 confirmed)
- Supply Chain: **Balanced** (EMP004 + EMP009 available)
- HR Tech: **-1 FTE surplus** (PRJ002 partially staffed, EMP007 underutilised)

**Actions Required:** Begin hiring process for 2 Cloud ERP consultants (lead time 12 weeks). Redeploy EMP007 to support PRJ001 admin workstream.
""",
        "What is our automation readiness?": """
**Joule Analysis — Automation Readiness Index**

SAP Joule + AI agent deployment readiness across workforce:

| Dimension | Score | Benchmark |
|---|---|---|
| Data Quality (SuccessFactors) | 78/100 | Industry avg: 71 |
| Process Standardisation | 65/100 | Needs improvement |
| Employee Digital Literacy | 72/100 | Solid foundation |
| Change Management Maturity | 58/100 | Investment needed |
| **Overall Readiness** | **68/100** | **Moderate-High** |

**Top 3 Automation Opportunities:** (1) Payroll exception processing, (2) Leave & absence management, (3) Standard financial reporting.

**Investment Required:** €240K for tooling + reskilling.
**Projected Annual Saving:** €380K (Year 1 net positive: €140K).
"""
    }

    if user_q:
        matched = None
        for key in JOULE_RESPONSES:
            if any(w in user_q.lower() for w in key.lower().split()):
                matched = key
                break

        if matched:
            st.markdown(f"""
            <div style='background:#F0F7FF;border-left:4px solid #0070F2;padding:16px 20px;border-radius:0 8px 8px 0;margin:12px 0;'>
            <div style='font-size:12px;color:#0070F2;font-weight:700;margin-bottom:8px;'>🤖 JOULE · SAP Business AI</div>
            """, unsafe_allow_html=True)
            st.markdown(JOULE_RESPONSES[matched])
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background:#F0F7FF;border-left:4px solid #0070F2;padding:16px 20px;border-radius:0 8px 8px 0;margin:12px 0;'>
            <div style='font-size:12px;color:#0070F2;font-weight:700;margin-bottom:8px;'>🤖 JOULE · SAP Business AI</div>
            I've analysed your query across the SuccessFactors data layer, BTP AI models, and project pipeline. 
            For a more specific answer, try one of the quick-prompt options above, or connect to live SuccessFactors 
            data via the SAP BTP API integration.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Model transparency
    st.markdown("#### 🔬 AI Model Transparency")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.markdown("""<div class="sap-card">
        <div class="sap-card-header">Demand Forecasting</div>
        <b>Model:</b> Gradient Boosting (XGBoost)<br>
        <b>Features:</b> Pipeline warmth, historical win rates, project duration, skills demand index<br>
        <b>Accuracy:</b> 87% (RMSE: 1.3 FTEs)<br>
        <b>Training data:</b> 24 months historical
        </div>""", unsafe_allow_html=True)
    with col_t2:
        st.markdown("""<div class="sap-card">
        <div class="sap-card-header">Skills Matching</div>
        <b>Model:</b> BERT-based NLP (fine-tuned on HR taxonomy)<br>
        <b>Features:</b> Skills ontology, project requirements, performance ratings<br>
        <b>Match accuracy:</b> 91%<br>
        <b>Source:</b> SAP Skills Graph (SuccessFactors)
        </div>""", unsafe_allow_html=True)
    with col_t3:
        st.markdown("""<div class="sap-card">
        <div class="sap-card-header">Attrition Prediction</div>
        <b>Model:</b> Logistic Regression + SHAP explainability<br>
        <b>Features:</b> Engagement scores, salary bands, utilisation trends, tenure<br>
        <b>AUC:</b> 0.83<br>
        <b>Alert threshold:</b> >35% attrition probability
        </div>""", unsafe_allow_html=True)
