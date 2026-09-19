"""analytics.py - Cross-department analytics dashboards using Plotly."""

import pandas as pd
import streamlit as st
import plotly.express as px
from utils.helpers import df_query


def render():
    st.markdown("## 📊 Analytics")
    st.caption("Operational analytics derived from simulated hospital data.")

    # ---- Patient admissions over time ----
    patients = df_query("SELECT admission_date FROM patients")
    patients["date"] = pd.to_datetime(patients["admission_date"]).dt.date
    admissions_over_time = patients.groupby("date").size().reset_index(name="Admissions")
    fig1 = px.line(admissions_over_time, x="date", y="Admissions", markers=True,
                    title="Patient Admissions Over Time")
    st.plotly_chart(fig1, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        # ---- Bed occupancy ----
        beds = df_query("SELECT * FROM beds")
        beds["available"] = beds["total_beds"] - beds["occupied_beds"]
        fig2 = px.bar(
            beds, x="ward", y=["occupied_beds", "available"],
            title="Bed Occupancy by Ward",
            labels={"value": "Beds", "ward": "Ward", "variable": "Status"},
            color_discrete_sequence=["#d64545", "#1a9e5c"],
        )
        st.plotly_chart(fig2, width='stretch')

    with col2:
        # ---- Emergency cases by priority ----
        emer = df_query("SELECT priority, COUNT(*) as count FROM emergency_cases GROUP BY priority")
        fig3 = px.pie(emer, names="priority", values="count", title="Emergency Cases by Priority",
                      color="priority",
                      color_discrete_map={"Critical": "#d64545", "High": "#e08a1e",
                                          "Medium": "#e0c61e", "Low": "#1a9e5c"})
        st.plotly_chart(fig3, width='stretch')

    col3, col4 = st.columns(2)

    with col3:
        # ---- Laboratory workload ----
        lab = df_query("SELECT test_name, COUNT(*) as count FROM lab_tests GROUP BY test_name")
        fig4 = px.bar(lab, x="test_name", y="count", title="Laboratory Workload by Test Type",
                      labels={"test_name": "Test", "count": "Count"})
        fig4.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(fig4, width='stretch')

    with col4:
        # ---- Imaging workload ----
        imaging = df_query("SELECT scan_type, COUNT(*) as count FROM imaging_scans GROUP BY scan_type")
        fig5 = px.bar(imaging, x="scan_type", y="count", title="Imaging Workload by Scan Type",
                      labels={"scan_type": "Scan Type", "count": "Count"},
                      color_discrete_sequence=["#1668a5"])
        st.plotly_chart(fig5, width='stretch')

    # ---- Agent activity ----
    activity = df_query(
        "SELECT agent_name, COUNT(*) as count FROM agent_activity_log GROUP BY agent_name ORDER BY count DESC"
    )
    fig6 = px.bar(activity, x="agent_name", y="count", title="Agent Activity Volume",
                  labels={"agent_name": "Agent", "count": "Logged Activities"},
                  color_discrete_sequence=["#0b3d66"])
    fig6.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(fig6, width='stretch')
