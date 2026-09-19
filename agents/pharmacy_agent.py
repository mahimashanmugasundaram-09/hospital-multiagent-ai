"""pharmacy_agent.py - Monitors medicine inventory and low-stock conditions."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class PharmacyAgent(BaseAgent):
    name = "Pharmacy Agent"

    def analyze(self):
        conn = get_connection()
        low_stock = conn.execute(
            "SELECT name FROM medicines WHERE status = 'Low Stock'"
        ).fetchall()
        conn.close()

        low_stock_names = [row["name"] for row in low_stock]
        findings = {
            "agent": self.name,
            "metric": f"{len(low_stock_names)} medicines currently flagged as low stock.",
            "alert": len(low_stock_names) > 0,
            "alert_message": f"Low stock detected: {', '.join(low_stock_names)}."
            if low_stock_names else None,
        }
        return findings
