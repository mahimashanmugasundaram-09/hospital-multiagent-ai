"""nursing.py - Nursing workload and task assignment overview."""

import streamlit as st
import plotly.express as px
from utils.helpers import df_query


def render():
    st.markdown("## 👩‍⚕️ Nursing")
    st.caption("Simulated nursing workload monitored by the Nursing Coordination Agent.")

    df = df_query("SELECT * FROM nursing_tasks ORDER BY id DESC")

    col1, col2, col3 = st.columns(3)
    col1.metric("Pending", len(df[df["status"] == "Pending"]))
    col2.metric("In Progress", len(df[df["status"] == "In Progress"]))
    col3.metric("Completed", len(df[df["status"] == "Completed"]))

    workload = df.groupby("nurse_name").size().reset_index(name="Task Count")
    fig = px.bar(workload, x="nurse_name", y="Task Count", title="Task Load by Nurse",
                 labels={"nurse_name": "Nurse"})
    st.plotly_chart(fig, width='stretch')

    st.dataframe(
        df.rename(columns={
            "nurse_name": "Nurse", "task": "Task", "patient_name": "Patient",
            "status": "Status", "shift": "Shift",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )
