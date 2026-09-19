"""surgery.py - Operating room schedule and surgical case tracking."""

import streamlit as st
from utils.helpers import df_query


def render():
    st.markdown("## ⚕️ Surgery")
    st.caption("Simulated operating room schedule monitored by the Surgery Scheduling Agent.")

    df = df_query("SELECT * FROM surgeries ORDER BY scheduled_time DESC")

    col1, col2, col3 = st.columns(3)
    col1.metric("Scheduled", len(df[df["status"] == "Scheduled"]))
    col2.metric("In Progress", len(df[df["status"] == "In Progress"]))
    col3.metric("Completed", len(df[df["status"] == "Completed"]))

    st.dataframe(
        df.rename(columns={
            "patient_name": "Patient", "surgery_name": "Surgery", "operating_room": "Operating Room",
            "surgeon": "Surgeon", "priority": "Priority", "scheduled_time": "Scheduled Time",
            "status": "Status",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )
