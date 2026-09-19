"""treatment_agent.py - Coordinates treatment pathway planning for admitted patients."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class TreatmentAgent(BaseAgent):
    name = "Treatment Planning Agent"

    def analyze(self):
        conn = get_connection()
        in_treatment = conn.execute(
            "SELECT COUNT(*) c FROM patients WHERE current_stage = 'In Treatment'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{in_treatment} patients currently in active treatment pathways.",
            "alert": False,
            "alert_message": None,
        }
        return findings
