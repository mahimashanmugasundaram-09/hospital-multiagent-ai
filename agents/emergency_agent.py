"""emergency_agent.py - Monitors emergency department demand and triage."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class EmergencyAgent(BaseAgent):
    name = "Emergency Response Agent"

    def analyze(self):
        conn = get_connection()
        critical = conn.execute(
            "SELECT COUNT(*) c FROM emergency_cases WHERE priority = 'Critical' AND status != 'Resolved'"
        ).fetchone()["c"]
        active = conn.execute(
            "SELECT COUNT(*) c FROM emergency_cases WHERE status != 'Resolved'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{active} active emergency cases, {critical} flagged Critical priority.",
            "alert": critical > 0,
            "alert_message": f"{critical} critical emergency cases require immediate resource allocation."
            if critical > 0 else None,
        }
        return findings
