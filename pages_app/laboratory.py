"""laboratory.py - Pending and completed laboratory tests."""

import streamlit as st
from utils.helpers import df_query


def render():
    st.markdown("## 🧪 Laboratory")
    st.caption("Simulated lab test queue monitored by the Laboratory Testing Agent.")

    df = df_query("SELECT * FROM lab_tests ORDER BY requested_time DESC")

    col1, col2, col3 = st.columns(3)
    col1.metric("Pending Tests", len(df[df["status"] == "Pending"]))
    col2.metric("In Progress", len(df[df["status"] == "In Progress"]))
    col3.metric("Completed", len(df[df["status"] == "Completed"]))

    status_filter = st.multiselect("Filter by status", sorted(df["status"].unique()))
    filtered = df[df["status"].isin(status_filter)] if status_filter else df

    st.dataframe(
        filtered.rename(columns={
            "patient_id": "Patient ID", "patient_name": "Patient", "test_name": "Test",
            "priority": "Priority", "status": "Status", "requested_time": "Requested At",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )
