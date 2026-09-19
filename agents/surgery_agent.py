"""surgery_agent.py - Manages operating room scheduling and surgical priorities."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class SurgeryAgent(BaseAgent):
    name = "Surgery Scheduling Agent"

    def analyze(self):
        conn = get_connection()
        scheduled = conn.execute(
            "SELECT COUNT(*) c FROM surgeries WHERE status = 'Scheduled'"
        ).fetchone()["c"]
        critical = conn.execute(
            "SELECT COUNT(*) c FROM surgeries WHERE priority = 'Critical' AND status != 'Completed'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{scheduled} surgeries scheduled, {critical} marked Critical priority.",
            "alert": critical > 0,
            "alert_message": f"{critical} critical-priority surgeries need operating room prioritization."
            if critical > 0 else None,
        }
        return findings
