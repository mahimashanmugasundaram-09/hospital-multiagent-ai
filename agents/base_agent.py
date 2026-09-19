"""
base_agent.py
Shared base class for all specialized hospital agents.
"""

from datetime import datetime
from database.database import get_connection


class BaseAgent:
    name = "Base Agent"

    def get_status(self):
        """Fetch this agent's status row from the database."""
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM agent_status WHERE agent_name = ?", (self.name,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def log_activity(self, activity_text):
        """Record an activity entry for this agent."""
        conn = get_connection()
        conn.execute(
            "INSERT INTO agent_activity_log (agent_name, activity, timestamp) VALUES (?, ?, ?)",
            (self.name, activity_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.execute(
            """UPDATE agent_status
               SET tasks_completed = tasks_completed + 1,
                   last_activity = ?
               WHERE agent_name = ?""",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.name),
        )
        conn.commit()
        conn.close()

    def analyze(self):
        """Override in subclasses. Should return a dict of findings."""
        raise NotImplementedError
