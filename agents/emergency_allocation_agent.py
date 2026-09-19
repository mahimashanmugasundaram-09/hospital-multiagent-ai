"""emergency_allocation_agent.py - Coordinates allocation of scarce emergency resources."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class EmergencyAllocationAgent(BaseAgent):
    name = "Emergency Allocation Agent"

    def analyze(self):
        conn = get_connection()
        rows = conn.execute(
            "SELECT required_resources, COUNT(*) c FROM emergency_cases "
            "WHERE status != 'Resolved' GROUP BY required_resources ORDER BY c DESC LIMIT 1"
        ).fetchone()
        conn.close()

        top_resource = rows["required_resources"] if rows else "N/A"
        top_count = rows["c"] if rows else 0

        findings = {
            "agent": self.name,
            "metric": f"Highest resource demand: {top_resource} ({top_count} active requests).",
            "alert": top_count >= 3,
            "alert_message": f"High demand detected for {top_resource} — {top_count} concurrent requests."
            if top_count >= 3 else None,
        }
        return findings
