"""
app.py
Entry point for the Hospital AI - Multi-Agent Operations Assistant.
Run with: python -m streamlit run app.py
"""

import streamlit as st

from database.database import init_database
from database.seed_data import seed_all
from utils.styles import load_css

from pages_app import (
    dashboard,
    patients,
    agents,
    emergency,
    laboratory,
    imaging,
    surgery,
    pharmacy,
    nursing,
    analytics,
    system_status,
)

st.set_page_config(
    page_title="Hospital AI - Multi-Agent Operations Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- DATABASE INITIALIZATION (idempotent) ----------------
init_database()
seed_all()

# ---------------- STYLES ----------------
load_css()

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.markdown("## 🏥 Hospital AI")
st.sidebar.caption("Multi-Agent Operations Assistant")
st.sidebar.write("---")

NAV_OPTIONS = {
    "🏠 Dashboard": dashboard,
    "👥 Patients": patients,
    "🤖 AI Agents": agents,
    "🚨 Emergency": emergency,
    "🧪 Laboratory": laboratory,
    "🖥️ Medical Imaging": imaging,
    "⚕️ Surgery": surgery,
    "💊 Pharmacy": pharmacy,
    "👩‍⚕️ Nursing": nursing,
    "📊 Analytics": analytics,
    "⚙️ System Status": system_status,
}

selection = st.sidebar.radio("Navigate", list(NAV_OPTIONS.keys()), label_visibility="collapsed")

st.sidebar.write("---")
st.sidebar.caption(
    "🩺 Operational decision support using simulated data only. "
    "Not a replacement for qualified healthcare professionals."
)

# ---------------- PAGE ROUTING ----------------
try:
    page_module = NAV_OPTIONS[selection]
    page_module.render()
except Exception as exc:  # pragma: no cover - defensive guard for demo stability
    st.error("Something went wrong while loading this page. Please try navigating again.")
    with st.expander("Technical details (for developers)"):
        st.exception(exc)
