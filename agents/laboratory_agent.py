"""laboratory_agent.py - Tracks pending lab tests and turnaround priorities."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class LaboratoryAgent(BaseAgent):
    name = "Laboratory Testing Agent"

    def analyze(self):
        conn = get_connection()
        pending = conn.execute(
            "SELECT COUNT(*) c FROM lab_tests WHERE status = 'Pending'"
        ).fetchone()["c"]
        critical = conn.execute(
            "SELECT COUNT(*) c FROM lab_tests WHERE priority = 'Critical' AND status != 'Completed'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{pending} lab tests pending, {critical} at Critical priority.",
            "alert": critical > 0,
            "alert_message": f"{critical} critical lab tests require expedited processing."
            if critical > 0 else None,
        }
        return findings
