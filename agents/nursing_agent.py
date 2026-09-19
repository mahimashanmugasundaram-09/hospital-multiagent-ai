"""nursing_agent.py - Balances nursing workload and task assignment across shifts."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class NursingAgent(BaseAgent):
    name = "Nursing Coordination Agent"

    def analyze(self):
        conn = get_connection()
        pending = conn.execute(
            "SELECT COUNT(*) c FROM nursing_tasks WHERE status = 'Pending'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{pending} nursing tasks currently pending assignment.",
            "alert": pending > 8,
            "alert_message": f"{pending} pending nursing tasks — workload may need rebalancing."
            if pending > 8 else None,
        }
        return findings
