"""patient_flow_agent.py - Monitors bed occupancy and overall patient flow through the hospital."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class PatientFlowAgent(BaseAgent):
    name = "Patient Flow Agent"

    def analyze(self):
        conn = get_connection()
        rows = conn.execute("SELECT total_beds, occupied_beds FROM beds").fetchall()
        conn.close()

        total = sum(r["total_beds"] for r in rows) if rows else 0
        occupied = sum(r["occupied_beds"] for r in rows) if rows else 0
        available = total - occupied
        occupancy_pct = round((occupied / total) * 100, 1) if total else 0

        findings = {
            "agent": self.name,
            "metric": f"Bed occupancy at {occupancy_pct}% ({available} beds available out of {total}).",
            "alert": occupancy_pct > 85,
            "alert_message": f"Bed occupancy critically high at {occupancy_pct}% — only {available} beds available."
            if occupancy_pct > 85 else None,
        }
        return findings
