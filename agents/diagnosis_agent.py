"""diagnosis_agent.py - Supports diagnosis review by cross-referencing lab and imaging results."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class DiagnosisAgent(BaseAgent):
    name = "Medical Diagnosis Support Agent"

    def analyze(self):
        conn = get_connection()
        pending_labs = conn.execute(
            "SELECT COUNT(*) c FROM lab_tests WHERE status != 'Completed'"
        ).fetchone()["c"]
        pending_scans = conn.execute(
            "SELECT COUNT(*) c FROM imaging_scans WHERE status != 'Completed'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"Cross-referencing {pending_labs} pending lab results and "
                      f"{pending_scans} pending imaging results for diagnosis support.",
            "alert": (pending_labs + pending_scans) > 15,
            "alert_message": "High volume of pending diagnostic data may delay diagnosis support."
            if (pending_labs + pending_scans) > 15 else None,
        }
        return findings
