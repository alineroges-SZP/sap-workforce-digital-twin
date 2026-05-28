# 🔷 SAP Workforce Digital Twin — Prototype Dashboard

**MBA Industry Project · Alex Chen · SAP SuccessFactors**

A Streamlit-based prototype demonstrating the **Workforce Digital Twin** concept: a simulation layer embedded within SAP SuccessFactors that enables organisations to model, test, and optimise workforce decisions *before* execution.

---

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/<your-username>/sap-workforce-digital-twin.git
cd sap-workforce-digital-twin

# 2. Install dependencies
pip install streamlit pandas numpy plotly

# 3. Run the dashboard
streamlit run workforce_digital_twin_dashboard.py
```

The app will open at `http://localhost:8501`

---

## 📐 What This Prototype Demonstrates

| Feature | Description |
|---|---|
| **Overview Dashboard** | Real-time KPIs — utilisation, pipeline value, headcount gaps, AI alerts |
| **Workforce Roster** | Employee profiles, skills, availability, 6-month allocation forecast |
| **Project Pipeline** | Gantt view, staffing gaps, warmth-based filtering (Cold/Warm/Hot/Sold) |
| **Scenario Simulation** | 3 pre-built What-If scenarios (see below) |
| **Joule AI Insights** | Simulated SAP Business AI recommendations on staffing and automation |

---

## 🔮 The 3 Simulation Scenarios

### Scenario A — Rapid Pipeline Growth (+30%)
> SAP wins 30% more projects than forecast. What is the headcount impact? Can we staff internally?

- Demand vs Supply forecast visualisation
- Headcount gap quantification by month
- Cost comparison: reskill vs hire vs partner network

### Scenario B — Internal Mobility vs. External Hiring
> Open positions on two projects. What is the optimal sourcing strategy?

- Side-by-side cost, time, and risk comparison
- AI verdict: hybrid approach with role-specific logic
- Training ROI calculation

### Scenario C — Automation Impact (Joule AI Agents)
> 30% of Finance and HR back-office tasks are automated via Joule. What happens to the workforce?

- 18-month automation impact curve
- Role-level task decomposition
- Reskilling investment vs cost efficiency gained
- Net ROI calculation

---

## 🏗️ Architecture Context

This dashboard is a **prototype representation** of a tool that would live natively inside SAP SuccessFactors, built on:

```
┌─────────────────────────────────────┐
│           Dashboard (UI)             │  ← This prototype (Streamlit → SAP Fiori in production)
├─────────────────────────────────────┤
│         AI Decision Layer            │  SAP Business AI / Joule
├─────────────────────────────────────┤
│       Simulation Engine (CORE)       │  Scenario modelling, cost projections, What-If
├─────────────────────────────────────┤
│      Workforce Intelligence          │  Skills matching (NLP), demand forecasting (XGBoost)
├─────────────────────────────────────┤
│           Data Layer                 │  SAP SuccessFactors + S/4HANA + BTP
└─────────────────────────────────────┘
```

**In production**, this tool would:
- Connect to live SuccessFactors APIs (Employee Central, Recruiting, LMS)
- Use SAP BTP AI Foundation for model hosting
- Be built as a SAP Fiori application (SAPUI5)
- Integrate with SAP Analytics Cloud for advanced visualisation

---

## 📦 Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
```

---

## 🎓 Academic Context

**Project:** Global Industry Project (GIP) — MBA Programme  
**Company Partner:** SAP SE  
**Topic:** A Conceptual Framework for Simulation-Based Workforce Strategy  
**Concept:** Workforce Digital Twin embedded in SAP SuccessFactors

---

## 📄 License

This prototype is for academic demonstration purposes only. SAP, SuccessFactors, Joule, and BTP are trademarks of SAP SE.
