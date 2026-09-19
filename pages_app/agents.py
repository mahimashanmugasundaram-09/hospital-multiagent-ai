"""agents.py - Detailed status view of all specialized agents plus the Chief Decision Agent."""

import streamlit as st
from utils.helpers import get_all_agent_status
from agents.chief_decision_agent import ChiefDecisionAgent


def render():
    st.markdown("## 🤖 AI Agents")
    st.caption("Sixteen specialized agents feed findings into the Chief Decision Agent, "
               "which coordinates hospital-wide operational decisions.")

    agent_df = get_all_agent_status()

    for row in agent_df.itertuples():
        is_chief = row.agent_name == "Chief Decision Agent"
        card_class = "agent-card chief" if is_chief else "agent-card"
        status_class = "status-active" if row.status == "Active" else "status-monitoring"
        icon = "👑" if is_chief else "🤖"
        st.markdown(
            f"""
            <div class="{card_class}">
                <b>{icon} {row.agent_name}</b><br>
                <span class="{status_class}">Status: {row.status}</span><br>
                Current Task: {row.current_task}<br>
                Tasks Completed: {row.tasks_completed}<br>
                Last Activity: {row.last_activity}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("---")
    st.markdown("### 🧠 Live Findings Feed")
    st.caption("Trigger a fresh analysis pass across every specialized agent.")

    if st.button("▶️ Run Full Agent Analysis"):
        chief = ChiefDecisionAgent()
        findings = chief.gather_findings()
        for f in findings:
            alert_icon = "🚨" if f["alert"] else "✅"
            st.markdown(f"**{alert_icon} {f['agent']}** — {f['metric']}")
            if f["alert_message"]:
                st.markdown(f"> ⚠️ {f['alert_message']}")
