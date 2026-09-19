"""imaging.py - CT, MRI, X-Ray and ultrasound scan queue."""

import streamlit as st
from utils.helpers import df_query


def render():
    st.markdown("## 🖥️ Medical Imaging")
    st.caption("Simulated imaging queue monitored by the Medical Imaging Agent.")

    df = df_query("SELECT * FROM imaging_scans ORDER BY scheduled_time DESC")

    scan_types = sorted(df["scan_type"].unique())
    tabs = st.tabs(["All"] + scan_types)

    with tabs[0]:
        _render_table(df)

    for i, scan_type in enumerate(scan_types, start=1):
        with tabs[i]:
            _render_table(df[df["scan_type"] == scan_type])


def _render_table(df):
    col1, col2, col3 = st.columns(3)
    col1.metric("Pending", len(df[df["status"] == "Pending"]))
    col2.metric("Scheduled", len(df[df["status"] == "Scheduled"]))
    col3.metric("Completed", len(df[df["status"] == "Completed"]))

    st.dataframe(
        df.rename(columns={
            "patient_id": "Patient ID", "patient_name": "Patient", "scan_type": "Scan Type",
            "priority": "Priority", "status": "Status", "scheduled_time": "Scheduled Time",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )
