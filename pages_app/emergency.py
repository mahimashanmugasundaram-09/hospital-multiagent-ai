"""emergency.py - Active emergency department cases and resource needs."""

import streamlit as st
from utils.helpers import df_query


def render():
    st.markdown("## 🚨 Emergency Department")
    st.caption("Simulated active emergency cases monitored by the Emergency Response Agent.")

    df = df_query("SELECT * FROM emergency_cases ORDER BY waiting_time_min DESC")

    critical = len(df[(df["priority"] == "Critical") & (df["status"] != "Resolved")])
    active = len(df[df["status"] != "Resolved"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Active Cases", active)
    col2.metric("Critical Priority", critical)
    col3.metric("Avg. Waiting Time (min)", round(df["waiting_time_min"].mean(), 1) if len(df) else 0)

    st.dataframe(
        df.rename(columns={
            "patient_name": "Patient", "priority": "Priority", "department": "Department",
            "required_resources": "Required Resources", "waiting_time_min": "Waiting Time (min)",
            "assigned_agent": "Assigned Agent", "status": "Status",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )
