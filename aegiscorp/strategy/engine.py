import uuid
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from aegiscorp.agents.deliberation import ExecutiveDeliberationCouncil
from aegiscorp.governance.policy import PolicyEngine
from aegiscorp.company.db import DatabaseManager

class DepartmentWorkstream(BaseModel):
    id: str
    department: str
    lead_role: str
    objective: str
    deliverables: List[str]
    budget: float
    target_kpis: List[str]

class StrategicProgram(BaseModel):
    id: str
    title: str
    objective_id: str
    total_budget: float
    workstreams: List[DepartmentWorkstream]
    status: str = "PLANNED"  # PLANNED, APPROVED, ACTIVE, COMPLETED

class StrategicObjective(BaseModel):
    id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    proposer_role_id: str = "ceo"
    target_timeline_months: int = 12
    capital_allocation: float = 0.0
    programs: List[StrategicProgram] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)

class StrategyEngine:
    """Translates high-level natural language objectives into governed strategic programs and departmental workstreams."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.council = ExecutiveDeliberationCouncil()
        self.policy_engine = PolicyEngine()

    def decompose_objective(self, objective_text: str, capital_budget: float = 25_000_000.0) -> StrategicObjective:
        obj = StrategicObjective(
            title=objective_text,
            description=f"Governed enterprise program for: {objective_text}",
            capital_allocation=capital_budget,
        )

        # 1. Executive Deliberation
        delib = self.council.deliberate(objective=objective_text, proposed_plan="Enterprise Strategic Program Decomposition", capital_amount=capital_budget)

        # 2. Decompose into departmental workstreams across Engineering, Product, Sales, Marketing, Finance, Operations, People
        prog_id = f"prog_{uuid.uuid4().hex[:8]}"
        workstreams = [
            DepartmentWorkstream(
                id=f"ws_eng_{uuid.uuid4().hex[:6]}",
                department="Engineering",
                lead_role="cto",
                objective="Deliver scalable zero-trust agentic security architecture and distributed runtime engine",
                deliverables=["Agent Runtime Core Engine", "Policy Enforcement Gateway", "Deterministic Tool Firewall"],
                budget=capital_budget * 0.35,
                target_kpis=["Availability: 99.99%", "Lead Time: <12h", "Change Failure Rate: <1%"],
            ),
            DepartmentWorkstream(
                id=f"ws_prod_{uuid.uuid4().hex[:6]}",
                department="Product",
                lead_role="cpo",
                objective="Define product roadmap, user flows, and enterprise management console",
                deliverables=["Enterprise Control Plane UI", "Real-time Org Chart Explorer", "Decision Audit Console"],
                budget=capital_budget * 0.15,
                target_kpis=["Activation Rate: >60%", "NPS: >70"],
            ),
            DepartmentWorkstream(
                id=f"ws_sales_{uuid.uuid4().hex[:6]}",
                department="Sales",
                lead_role="cro",
                objective="Execute enterprise GTM motion targeting Fortune 500 security leaders",
                deliverables=["Strategic Account Lists", "Enterprise POC Playbook", "Commercial Pricing Matrix"],
                budget=capital_budget * 0.20,
                target_kpis=["New ARR: +$50M", "Win Rate: >35%", "ACV: >$250k"],
            ),
            DepartmentWorkstream(
                id=f"ws_mktg_{uuid.uuid4().hex[:6]}",
                department="Marketing",
                lead_role="cmo",
                objective="Establish category authority and generate high-intent pipeline",
                deliverables=["Gartner/Forrester Analyst Briefings", "Autonomous Enterprise Whitepaper", "Benchmark Campaigns"],
                budget=capital_budget * 0.10,
                target_kpis=["Inbound SQLs: +300/mo", "Brand Reach: +100k views"],
            ),
            DepartmentWorkstream(
                id=f"ws_fin_{uuid.uuid4().hex[:6]}",
                department="Finance",
                lead_role="cfo",
                objective="Manage capital deployment, runway preservation, and investor reporting",
                deliverables=["Tranche Capital Release Schedule", "Cost-of-Capital Optimization", "Audit-Ready Models"],
                budget=capital_budget * 0.05,
                target_kpis=["Runway: >24 months", "Gross Margin: >80%"],
            ),
            DepartmentWorkstream(
                id=f"ws_ops_{uuid.uuid4().hex[:6]}",
                department="Operations",
                lead_role="coo",
                objective="Establish operating cadence, cross-functional SLAs, and delivery monitoring",
                deliverables=["Weekly Executive Cadence Deck", "SLA Dashboards", "Disaster Recovery Runbooks"],
                budget=capital_budget * 0.10,
                target_kpis=["SLA Adherence: >98%", "Process Velocity: +40%"],
            ),
            DepartmentWorkstream(
                id=f"ws_people_{uuid.uuid4().hex[:6]}",
                department="People",
                lead_role="chro",
                objective="Attract elite PhD/Gold-Medalist tier engineering and product talent",
                deliverables=["Targeted Hiring Pipeline", "Technical Competency Rubric", "Competitive Equity Grants"],
                budget=capital_budget * 0.05,
                target_kpis=["Time-to-Hire: <30 days", "Critical-Skill Coverage: >95%"],
            ),
        ]

        program = StrategicProgram(
            id=prog_id,
            title=f"Program: {objective_text}",
            objective_id=obj.id,
            total_budget=capital_budget,
            workstreams=workstreams,
            status="APPROVED",
        )
        obj.programs.append(program)

        # Record in database
        self.db.record_event(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            event_type="objective_created",
            aggregate_id=obj.id,
            actor="ceo",
            payload={"title": obj.title, "budget": capital_budget, "programs": len(obj.programs)},
        )

        return obj
