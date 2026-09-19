"""patients.py - Displays simulated patient records with filtering."""

import streamlit as st
from utils.helpers import df_query


def render():
    st.markdown("## 👥 Patients")
    st.caption("Simulated patient records for demonstration purposes only. No real patient information is used.")

    df = df_query("SELECT * FROM patients ORDER BY admission_date DESC")

    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.multiselect("Department", sorted(df["department"].unique()))
    with col2:
        priority_filter = st.multiselect("Priority", sorted(df["priority"].unique()))
    with col3:
        status_filter = st.multiselect("Admission Status", sorted(df["admission_status"].unique()))

    filtered = df.copy()
    if dept_filter:
        filtered = filtered[filtered["department"].isin(dept_filter)]
    if priority_filter:
        filtered = filtered[filtered["priority"].isin(priority_filter)]
    if status_filter:
        filtered = filtered[filtered["admission_status"].isin(status_filter)]

    st.dataframe(
        filtered.rename(columns={
            "patient_id": "Patient ID", "name": "Name", "age": "Age", "gender": "Gender",
            "department": "Department", "priority": "Priority",
            "admission_status": "Admission Status", "assigned_bed": "Assigned Bed",
            "current_stage": "Current Stage", "admission_date": "Admission Date",
        }),
        width='stretch',
        hide_index=True,
    )

    st.info(f"Showing {len(filtered)} of {len(df)} patient records.")
