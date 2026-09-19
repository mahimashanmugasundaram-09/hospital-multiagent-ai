"""blood_inventory_agent.py - Monitors blood bank stock levels across blood types."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class BloodInventoryAgent(BaseAgent):
    name = "Blood Inventory Agent"

    def analyze(self):
        conn = get_connection()
        critical = conn.execute(
            "SELECT blood_type FROM blood_inventory WHERE status = 'Critical'"
        ).fetchall()
        conn.close()

        critical_types = [r["blood_type"] for r in critical]
        findings = {
            "agent": self.name,
            "metric": f"{len(critical_types)} blood types at critical stock levels.",
            "alert": len(critical_types) > 0,
            "alert_message": f"Critical shortage in blood types: {', '.join(critical_types)}."
            if critical_types else None,
        }
        return findings
