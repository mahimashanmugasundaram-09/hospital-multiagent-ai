"""imaging_agent.py - Schedules and tracks CT, MRI, X-Ray, and ultrasound workload."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class ImagingAgent(BaseAgent):
    name = "Medical Imaging Agent"

    def analyze(self):
        conn = get_connection()
        pending = conn.execute(
            "SELECT COUNT(*) c FROM imaging_scans WHERE status = 'Pending'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{pending} imaging scans pending scheduling or completion.",
            "alert": pending > 6,
            "alert_message": f"{pending} pending scans — imaging queue is building up."
            if pending > 6 else None,
        }
        return findings
