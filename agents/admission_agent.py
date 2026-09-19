"""admission_agent.py - Monitors patient admissions and registration flow."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class AdmissionAgent(BaseAgent):
    name = "Patient Admission Agent"

    def analyze(self):
        conn = get_connection()
        total = conn.execute("SELECT COUNT(*) c FROM patients").fetchone()["c"]
        waiting = conn.execute(
            "SELECT COUNT(*) c FROM patients WHERE admission_status = 'Waiting'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{total} total patients on record, {waiting} awaiting admission processing.",
            "alert": waiting > 5,
            "alert_message": f"{waiting} patients waiting on admission — consider expediting registration."
            if waiting > 5 else None,
        }
        return findings
