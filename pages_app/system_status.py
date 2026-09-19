"""system_status.py - Overall system health, database status, and compliance log."""

import os
import streamlit as st
from utils.helpers import df_query, get_all_agent_status
from database.database import DB_PATH


def render():
    st.markdown("## ⚙️ System Status")
    st.caption("Technical health overview of the Hospital AI platform.")

    col1, col2, col3 = st.columns(3)
    with col1:
        db_exists = os.path.exists(DB_PATH)
        st.metric("Database", "Connected ✅" if db_exists else "Not Found ❌")
    with col2:
        agent_df = get_all_agent_status()
        active_count = len(agent_df[agent_df["status"] == "Active"])
        st.metric("Active Agents", f"{active_count} / {len(agent_df)}")
    with col3:
        decisions = df_query("SELECT COUNT(*) c FROM decisions")
        st.metric("Decisions Logged", int(decisions.iloc[0]["c"]))

    st.write("---")
    st.markdown("### 🔒 Compliance & Data Security Log")
    compliance = df_query("SELECT * FROM compliance_log ORDER BY id DESC")
    st.dataframe(
        compliance.rename(columns={
            "check_type": "Check Type", "status": "Status",
            "details": "Details", "timestamp": "Timestamp",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )

    st.write("---")
    st.markdown("### 🩸 Blood Inventory Status")
    blood = df_query("SELECT * FROM blood_inventory ORDER BY units_available ASC")
    st.dataframe(
        blood.rename(columns={
            "blood_type": "Blood Type", "units_available": "Units Available", "status": "Status",
        }),
        width='stretch',
        hide_index=True,
    )

    st.write("---")
    st.markdown("### 🫀 Organ Inventory & Matching")
    organ = df_query("SELECT * FROM organ_inventory ORDER BY id ASC")
    st.dataframe(
        organ.rename(columns={
            "organ_type": "Organ", "status": "Status",
            "match_status": "Match Status", "location": "Location",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )

    st.write("---")
    st.markdown("### 🔬 Screening Programs")
    screening = df_query("SELECT * FROM screenings ORDER BY id DESC")
    st.dataframe(
        screening.rename(columns={
            "patient_name": "Patient", "screening_type": "Screening Type",
            "status": "Status", "result": "Result",
        }).drop(columns=["id"]),
        width='stretch',
        hide_index=True,
    )

    st.info("This system uses simulated data only. It is a hackathon operational "
            "decision-support prototype and is not connected to any real hospital records.")
