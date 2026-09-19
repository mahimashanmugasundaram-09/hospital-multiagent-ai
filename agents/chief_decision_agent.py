"""
chief_decision_agent.py
The central coordination layer. Gathers findings from every specialized
agent, detects conflicts/urgent issues, and produces an explainable,
prioritized action plan that indicates whether human approval is required.
"""

from datetime import datetime
from database.database import get_connection
from agents.base_agent import BaseAgent

from agents.admission_agent import AdmissionAgent
from agents.emergency_agent import EmergencyAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.treatment_agent import TreatmentAgent
from agents.pharmacy_agent import PharmacyAgent
from agents.surgery_agent import SurgeryAgent
from agents.nursing_agent import NursingAgent
from agents.laboratory_agent import LaboratoryAgent
from agents.imaging_agent import ImagingAgent
from agents.patient_flow_agent import PatientFlowAgent
from agents.blood_inventory_agent import BloodInventoryAgent
from agents.organ_inventory_agent import OrganInventoryAgent
from agents.screening_agent import ScreeningAgent
from agents.emergency_allocation_agent import EmergencyAllocationAgent
from agents.compliance_agent import ComplianceAgent


class ChiefDecisionAgent(BaseAgent):
    name = "Chief Decision Agent"

    def __init__(self):
        self.specialist_agents = [
            AdmissionAgent(),
            EmergencyAgent(),
            DiagnosisAgent(),
            TreatmentAgent(),
            PharmacyAgent(),
            SurgeryAgent(),
            NursingAgent(),
            LaboratoryAgent(),
            ImagingAgent(),
            PatientFlowAgent(),
            BloodInventoryAgent(),
            OrganInventoryAgent(),
            ScreeningAgent(),
            EmergencyAllocationAgent(),
            ComplianceAgent(),
        ]

    def gather_findings(self):
        """Collect analyze() output from every specialized agent."""
        return [agent.analyze() for agent in self.specialist_agents]

    def coordinate(self):
        """
        Aggregate findings, detect the highest-priority issue(s), and
        build an explainable recommended action plan.
        """
        findings = self.gather_findings()
        alerts = [f for f in findings if f.get("alert")]

        if len(alerts) >= 3:
            priority = "CRITICAL"
        elif len(alerts) >= 1:
            priority = "HIGH"
        else:
            priority = "NORMAL"

        contributing_agents = [f["agent"] for f in alerts] if alerts else \
            [f["agent"] for f in findings[:4]]

        if alerts:
            situation = " ".join(f["alert_message"] for f in alerts if f["alert_message"])
        else:
            situation = ("All monitored operations are within normal parameters. "
                         "No urgent conflicts detected across agents.")

        recommendation = self._build_recommendation(alerts)
        human_approval_required = priority in ("CRITICAL", "HIGH")

        conn = get_connection()
        conn.execute(
            """INSERT INTO decisions
               (priority, situation, agents_consulted, recommendation, human_approval, status, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                priority,
                situation,
                ", ".join(contributing_agents),
                recommendation,
                "Required" if human_approval_required else "Not Required",
                "Awaiting Human Approval" if human_approval_required else "Auto-Resolved",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()

        self.log_activity("Generated coordination plan across specialized agents")

        return {
            "priority": priority,
            "situation": situation,
            "agents_consulted": contributing_agents,
            "recommendation": recommendation,
            "human_approval": "Required" if human_approval_required else "Not Required",
            "status": "Awaiting Human Approval" if human_approval_required else "Auto-Resolved",
            "raw_findings": findings,
        }

    @staticmethod
    def _build_recommendation(alerts):
        if not alerts:
            return ("Continue standard monitoring across all departments. "
                    "No immediate action required.")
        actions = []
        for a in alerts:
            actions.append(f"Address findings from {a['agent']}")
        return "; ".join(actions) + ". Escalate to on-duty coordinator for human sign-off."

    def get_recent_decisions(self, limit=10):
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM decisions ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
