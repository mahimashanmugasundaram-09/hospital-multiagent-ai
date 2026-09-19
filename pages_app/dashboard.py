"""
dashboard.py
The Hospital Command Center - main landing page with KPIs, the Chief
Decision Agent panel, decision workflow, agent status grid, and activity log.
"""

import random
import streamlit as st
from utils.helpers import get_kpis, get_all_agent_status, get_recent_activity, priority_badge
from agents.chief_decision_agent import ChiefDecisionAgent


def render():
    st.markdown(
        """
        <div class="hai-header">
            <h1>🏥 Hospital Command Center</h1>
            <p>Real-time operational overview — powered by the Multi-Agent AI System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- KPI CARDS ----------------
    kpis = get_kpis()
    kpi_items = [
        ("Total Patients", kpis["total_patients"]),
        ("Today's Admissions", kpis["today_admissions"]),
        ("Available Beds", kpis["available_beds"]),
        ("Emergency Cases", kpis["emergency_cases"]),
        ("Pending Lab Tests", kpis["pending_labs"]),
        ("Pending Imaging", kpis["pending_imaging"]),
        ("Scheduled Surgeries", kpis["scheduled_surgeries"]),
        ("Low Stock Medicines", kpis["low_stock_meds"]),
    ]

    cols = st.columns(4)
    for i, (label, value) in enumerate(kpi_items):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if i % 4 == 3 and i != len(kpi_items) - 1:
            cols = st.columns(4)

    st.write("")

    # ---------------- CHIEF DECISION AGENT PANEL ----------------
    if "chief_agent" not in st.session_state:
        st.session_state.chief_agent = ChiefDecisionAgent()
    if "last_decision" not in st.session_state:
        st.session_state.last_decision = None

    chief = st.session_state.chief_agent

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("### 👑 Chief Decision Agent")
    with col_b:
        run_now = st.button("🔄 Run Coordination Cycle", width='stretch')

    if run_now or st.session_state.last_decision is None:
        st.session_state.last_decision = chief.coordinate()

    decision = st.session_state.last_decision
    active_decisions = random.randint(2, 5)

    st.markdown(
        f"""
        <div class="chief-panel">
            <span class="chief-badge">Status: ACTIVE</span>
            <span class="chief-badge">Coordination Mode: Multi-Agent Coordination</span>
            <span class="chief-badge">Agents Coordinated: 16</span>
            <span class="chief-badge">Active Decisions: {active_decisions}</span>
            <span class="chief-badge">Human Approval: {decision['human_approval'].upper()}</span>
            <h2>Current Coordination</h2>
            <p>Monitoring emergency demand, bed availability, diagnostics, imaging, staffing and patient flow.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- DECISION WORKFLOW ----------------
    st.markdown("### 🔄 Decision Workflow")
    workflow_steps = [
        "Hospital Data", "Specialized Agents", "Chief Decision Agent",
        "Conflict Detection", "Priority Assessment", "Recommended Action",
        "Human Approval", "Execution & Monitoring",
    ]
    st.markdown(
        " &nbsp;→&nbsp; ".join(f"**{step}**" for step in workflow_steps)
    )

    st.write("")

    # ---------------- CURRENT DECISION ----------------
    st.markdown("### 📋 Current Decision")
    st.markdown(
        f"""
        <div class="decision-card">
            <h4>Priority: {priority_badge(decision['priority'])}</h4>
            <p><b>Situation:</b><br>{decision['situation']}</p>
            <p><b>Agents consulted:</b><br>{', '.join(decision['agents_consulted']) if decision['agents_consulted'] else 'None'}</p>
            <p><b>Recommendation:</b><br>{decision['recommendation']}</p>
            <p><b>Human Approval:</b> {decision['human_approval']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("⚠️ This is simulated demo data generated for the hackathon prototype — not real hospital data.")

    if decision["human_approval"] == "Required":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Recommendation"):
                st.success("Decision approved by human operator. Execution simulated.")
        with c2:
            if st.button("❌ Reject Recommendation"):
                st.warning("Decision rejected. Escalated for manual review.")

    st.write("")

    # ---------------- AGENT STATUS GRID ----------------
    st.markdown("### 🤖 Agent Status Overview")
    agent_df = get_all_agent_status()
    grid_cols = st.columns(4)
    for idx, row in enumerate(agent_df.itertuples()):
        is_chief = row.agent_name == "Chief Decision Agent"
        card_class = "agent-card chief" if is_chief else "agent-card"
        status_class = "status-active" if row.status == "Active" else "status-monitoring"
        icon = "👑" if is_chief else "🤖"
        with grid_cols[idx % 4]:
            st.markdown(
                f"""
                <div class="{card_class}">
                    <b>{icon} {row.agent_name}</b><br>
                    <span class="{status_class}">{row.status}</span><br>
                    <small>{row.current_task}</small><br>
                    <small>Tasks completed: {row.tasks_completed}</small><br>
                    <small>Last activity: {row.last_activity}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # ---------------- ACTIVITY LOG ----------------
    st.markdown("### 🗒️ Recent Activity Log")
    activity_df = get_recent_activity(12)
    for row in activity_df.itertuples():
        st.markdown(f"- **{row.agent_name}** — {row.activity} _({row.timestamp})_")

    # ---------------- SAFETY NOTICE ----------------
    st.markdown(
        """
        <div class="safety-notice">
            🩺 <b>Clinical Safety Notice:</b><br>
            This system provides AI-assisted operational decision support using simulated data.
            Final clinical decisions remain with qualified healthcare professionals.
        </div>
        """,
        unsafe_allow_html=True,
    )
