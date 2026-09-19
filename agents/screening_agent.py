"""screening_agent.py - Monitors preventive and pre-procedural screening programs."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class ScreeningAgent(BaseAgent):
    name = "Testing & Screening Agent"

    def analyze(self):
        conn = get_connection()
        needs_review = conn.execute(
            "SELECT COUNT(*) c FROM screenings WHERE result = 'Requires Review'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{needs_review} screening results flagged as requiring review.",
            "alert": needs_review > 0,
            "alert_message": f"{needs_review} screening results require clinical review."
            if needs_review > 0 else None,
        }
        return findings
