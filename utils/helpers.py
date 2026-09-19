"""
helpers.py
Shared helper functions for querying data used by multiple pages.
"""

import pandas as pd
from database.database import get_connection

AGENT_ORDER = [
    "Chief Decision Agent",
    "Patient Admission Agent",
    "Emergency Response Agent",
    "Medical Diagnosis Support Agent",
    "Treatment Planning Agent",
    "Pharmacy Agent",
    "Surgery Scheduling Agent",
    "Nursing Coordination Agent",
    "Laboratory Testing Agent",
    "Medical Imaging Agent",
    "Patient Flow Agent",
    "Blood Inventory Agent",
    "Organ Inventory & Matching Agent",
    "Testing & Screening Agent",
    "Emergency Allocation Agent",
    "Compliance & Data Security Agent",
]


def df_query(query, params=None):
    """Run a SQL query and return the results as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params or [])
    conn.close()
    return df


def get_kpis():
    """Compute the top-level KPI values shown on the dashboard."""
    total_patients = df_query("SELECT COUNT(*) c FROM patients").iloc[0]["c"]
    today_admissions = df_query(
        "SELECT COUNT(*) c FROM patients WHERE date(admission_date) = date('now')"
    ).iloc[0]["c"]

    beds = df_query("SELECT SUM(total_beds) t, SUM(occupied_beds) o FROM beds")
    total_beds = beds.iloc[0]["t"] or 0
    occupied_beds = beds.iloc[0]["o"] or 0
    available_beds = int(total_beds - occupied_beds)

    emergency_cases = df_query(
        "SELECT COUNT(*) c FROM emergency_cases WHERE status != 'Resolved'"
    ).iloc[0]["c"]
    pending_labs = df_query(
        "SELECT COUNT(*) c FROM lab_tests WHERE status != 'Completed'"
    ).iloc[0]["c"]
    pending_imaging = df_query(
        "SELECT COUNT(*) c FROM imaging_scans WHERE status != 'Completed'"
    ).iloc[0]["c"]
    scheduled_surgeries = df_query(
        "SELECT COUNT(*) c FROM surgeries WHERE status = 'Scheduled'"
    ).iloc[0]["c"]
    low_stock_meds = df_query(
        "SELECT COUNT(*) c FROM medicines WHERE status = 'Low Stock'"
    ).iloc[0]["c"]

    return {
        "total_patients": int(total_patients),
        "today_admissions": int(today_admissions),
        "available_beds": available_beds,
        "emergency_cases": int(emergency_cases),
        "pending_labs": int(pending_labs),
        "pending_imaging": int(pending_imaging),
        "scheduled_surgeries": int(scheduled_surgeries),
        "low_stock_meds": int(low_stock_meds),
    }


def get_all_agent_status():
    """Return agent status rows ordered with Chief Decision Agent first."""
    df = df_query("SELECT * FROM agent_status")
    df["sort_order"] = df["agent_name"].apply(
        lambda x: AGENT_ORDER.index(x) if x in AGENT_ORDER else len(AGENT_ORDER)
    )
    df = df.sort_values("sort_order").drop(columns=["sort_order"])
    return df


def get_recent_activity(limit=15):
    return df_query(
        "SELECT * FROM agent_activity_log ORDER BY id DESC LIMIT ?", (limit,)
    )


def priority_badge(priority):
    """Return an emoji-prefixed label for a given priority string."""
    mapping = {
        "Critical": "🔴 Critical",
        "CRITICAL": "🔴 CRITICAL",
        "High": "🟠 High",
        "HIGH": "🟠 HIGH",
        "Medium": "🟡 Medium",
        "Low": "🟢 Low",
        "NORMAL": "🟢 NORMAL",
    }
    return mapping.get(priority, priority)
