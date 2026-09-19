"""compliance_agent.py - Audits data handling and compliance checks across the system."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    name = "Compliance & Data Security Agent"

    def analyze(self):
        conn = get_connection()
        failed = conn.execute(
            "SELECT COUNT(*) c FROM compliance_log WHERE status != 'Passed'"
        ).fetchone()["c"]
        total_checks = conn.execute("SELECT COUNT(*) c FROM compliance_log").fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{total_checks} compliance checks logged, {failed} flagged for attention.",
            "alert": failed > 0,
            "alert_message": f"{failed} compliance checks require attention." if failed > 0 else None,
        }
        return findings
