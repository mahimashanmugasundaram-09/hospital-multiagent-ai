"""organ_inventory_agent.py - Tracks organ availability and donor-recipient matching status."""

from database.database import get_connection
from agents.base_agent import BaseAgent


class OrganInventoryAgent(BaseAgent):
    name = "Organ Inventory & Matching Agent"

    def analyze(self):
        conn = get_connection()
        searching = conn.execute(
            "SELECT COUNT(*) c FROM organ_inventory WHERE match_status = 'Searching'"
        ).fetchone()["c"]
        conn.close()

        findings = {
            "agent": self.name,
            "metric": f"{searching} organs currently awaiting recipient matching.",
            "alert": searching > 2,
            "alert_message": f"{searching} organs still searching for a match — time-sensitive."
            if searching > 2 else None,
        }
        return findings
