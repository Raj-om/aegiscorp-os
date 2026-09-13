import os
import uuid
import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.org.graph import AuthorityGraph
from aegiscorp.governance.policy import PolicyEngine
from aegiscorp.governance.approval import ApprovalService, ApprovalStatus
from aegiscorp.governance.risk import RiskEngine
from aegiscorp.company.state import get_default_company_state, CompanyDigitalTwinState
from aegiscorp.company.db import DatabaseManager
from aegiscorp.kpi.tower import KPIControlTower
from aegiscorp.strategy.engine import StrategyEngine
from aegiscorp.execution.loop import ResearchExecutionLoop
from aegiscorp.execution.task_graph import ExecutionTaskGraph, ExecutionTask, TaskStatus
from aegiscorp.execution.tools import ToolGateway
from aegiscorp.finance.investment import InvestmentResearchEngine
from aegiscorp.simulation.scenario_engine import ScenarioEngine, SimulationRequest
from aegiscorp.agents.runtime import AgentRuntime, AgentTurnRequest
from aegiscorp.training import TrainingTournamentEngine, get_curriculum, get_all_curricula
from aegiscorp.ui import INDEX_HTML

def create_app() -> FastAPI:
    app = FastAPI(
        title="AegisCorp OS",
        version="1.0.0",
        description="Governed Multi-Agent Corporate Digital Twin and Enterprise Operating System",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Core singletons
    db = DatabaseManager()
    org_graph = AuthorityGraph()
    policy_engine = PolicyEngine()
    risk_engine = RiskEngine()
    approval_service = ApprovalService()
    kpi_tower = KPIControlTower()
    strategy_engine = StrategyEngine(db=db)
    research_loop = ResearchExecutionLoop(db=db)
    task_graph = ExecutionTaskGraph()
    tool_gateway = ToolGateway()
    investment_engine = InvestmentResearchEngine(db=db)
    scenario_engine = ScenarioEngine()
    agent_runtime = AgentRuntime(
        db_manager=db,
        policy_engine=policy_engine,
        risk_engine=risk_engine,
        approval_service=approval_service,
    )
    training_engine = TrainingTournamentEngine(db=db)

    # Seed initial digital twin state
    company_state = get_default_company_state()

    # Schemas
    class ObjectivePayload(BaseModel):
        title: str
        budget: float = 25_000_000.0

    class DecisionPayload(BaseModel):
        objective: str
        proposer_role_id: str
        capital_amount: float = 0.0
        is_legal_contract: bool = False
        involves_external_api: bool = False
        is_production_change: bool = False
        is_ma_transaction: bool = False
        payload: Optional[Dict[str, Any]] = None

    class ApprovalPayload(BaseModel):
        approver_role_id: str
        approved: bool = True
        rationale: str = "Authorized by designated executive."

    class PlanPayload(BaseModel):
        objective_id: str
        phases: List[str]

    class TaskAssignmentPayload(BaseModel):
        title: str
        description: str
        owner_role_id: str
        dependencies: List[str] = Field(default_factory=list)
        budget: float = 0.0
        deadline: Optional[str] = None

    class ResearchPayload(BaseModel):
        topic: str

    class TradePayload(BaseModel):
        symbol: str
        action: str = "BUY"
        amount_usd: float = 100_000.0
        price: float = 500.0

    class TrainingRunPayload(BaseModel):
        role_id: Optional[str] = None
        enterprise_wide: bool = False

    # -------------------------------------------------------------
    # REST API ENDPOINTS
    # -------------------------------------------------------------

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "version": "1.0.0",
            "service": "AegisCorp OS",
            "governance_mode": "STRICT",
            "timestamp": time.time(),
        }

    @app.get("/", response_class=HTMLResponse)
    def index():
        if os.path.exists(INDEX_HTML):
            with open(INDEX_HTML, "r", encoding="utf-8") as f:
                return f.read()
        return "<h1>AegisCorp OS API Operational</h1>"

    @app.get("/company/state")
    def get_state():
        return company_state

    @app.get("/org")
    def get_org():
        return {
            "total_roles": len(ALL_ROLES),
            "roles": [r.model_dump() for r in ALL_ROLES.values()],
            "graph": org_graph.export_graph_dict(),
        }

    @app.get("/kpis")
    def get_kpis():
        return {"kpis": [m.model_dump() for m in kpi_tower.get_all_metrics()]}

    @app.get("/audit")
    def get_audit(limit: int = 100):
        return {"events": db.get_events(limit=limit)}

    @app.post("/objectives")
    def create_objective(payload: ObjectivePayload):
        obj = strategy_engine.decompose_objective(
            objective_text=payload.title,
            capital_budget=payload.budget,
        )
        return obj.model_dump()

    @app.post("/decisions")
    def submit_decision(payload: DecisionPayload):
        turn_req = AgentTurnRequest(
            agent_id=f"agent_{payload.proposer_role_id}",
            role_id=payload.proposer_role_id,
            objective=payload.objective,
            task=f"Evaluate and execute: {payload.objective}",
            capital_amount=payload.capital_amount,
            is_legal_contract=payload.is_legal_contract,
            involves_external_api=payload.involves_external_api,
            is_production_change=payload.is_production_change,
            is_ma_transaction=payload.is_ma_transaction,
        )
        resp = agent_runtime.execute_turn(turn_req)
        db.save_decision({
            "id": resp.turn_id,
            "objective": payload.objective,
            "proposer": payload.proposer_role_id,
            "owner": payload.proposer_role_id,
            "status": resp.status,
            "risk": resp.risk_assessment.composite_score,
            "amount": payload.capital_amount,
            "payload": resp.structured_output,
            "created_at": time.time(),
        })
        return resp.model_dump()

    @app.get("/decisions/{id}")
    def get_decision(id: str):
        d = db.get_decision(id)
        if not d:
            raise HTTPException(status_code=404, detail="Decision not found")
        return d

    @app.post("/decisions/{id}/approve")
    def approve_decision(id: str, payload: ApprovalPayload):
        # Find pending approval request matching decision
        req_to_approve = None
        for req in approval_service.requests.values():
            if req.decision_id == id:
                req_to_approve = req
                break

        if not req_to_approve:
            raise HTTPException(status_code=404, detail="No active approval request found for this decision")

        try:
            updated = approval_service.record_approval(
                request_id=req_to_approve.id,
                approver_role_id=payload.approver_role_id,
                approved=payload.approved,
                rationale=payload.rationale,
            )
            # Record audit event
            db.record_event(
                event_id=f"evt_{uuid.uuid4().hex[:10]}",
                event_type="decision_approval_recorded",
                aggregate_id=id,
                actor=payload.approver_role_id,
                payload={
                    "approved": payload.approved,
                    "rationale": payload.rationale,
                    "overall_status": updated.status.value,
                },
            )
            return updated.model_dump()
        except PermissionError as pe:
            raise HTTPException(status_code=403, detail=str(pe))

    @app.post("/plans")
    def create_plan(payload: PlanPayload):
        plan_id = f"plan_{uuid.uuid4().hex[:8]}"
        db.record_event(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            event_type="plan_committed",
            aggregate_id=plan_id,
            actor="strategy_engine",
            payload={"objective_id": payload.objective_id, "phases": payload.phases},
        )
        return {"plan_id": plan_id, "status": "COMMITTED", "phases": payload.phases}

    @app.post("/agents/{id}/tasks")
    def assign_agent_task(id: str, payload: TaskAssignmentPayload):
        task = ExecutionTask(
            plan_id=id,
            owner_role_id=payload.owner_role_id,
            title=payload.title,
            description=payload.description,
            dependencies=payload.dependencies,
            budget=payload.budget,
            deadline=payload.deadline,
        )
        added = task_graph.add_task(task)
        db.record_event(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            event_type="task_assigned",
            aggregate_id=task.id,
            actor=id,
            payload={"owner": payload.owner_role_id, "title": payload.title, "budget": payload.budget},
        )
        return added.model_dump()

    @app.post("/simulations")
    def run_simulation(payload: SimulationRequest):
        res = scenario_engine.run_simulation(payload, base_state=company_state)
        return res.model_dump()

    @app.post("/research")
    def run_research(payload: ResearchPayload):
        res = research_loop.discover_and_compare(payload.topic)
        return res.model_dump()

    @app.get("/portfolio")
    def get_portfolio():
        return investment_engine.get_portfolio_summary()

    @app.post("/trade")
    def execute_trade(payload: TradePayload):
        order = investment_engine.execute_paper_trade(
            symbol=payload.symbol,
            action=payload.action,
            amount_usd=payload.amount_usd,
            current_price=payload.price,
        )
        return order.model_dump()

    # -------------------------------------------------------------
    # AGENT ACADEMY & TRAINING ENDPOINTS
    # -------------------------------------------------------------

    @app.post("/training/run")
    def run_training_tournament(payload: TrainingRunPayload):
        if payload.enterprise_wide or not payload.role_id:
            results = training_engine.run_enterprise_tournament()
            return {
                "status": "ENTERPRISE_TOURNAMENT_COMPLETED",
                "total_roles_evaluated": len(results),
                "gold_medals": sum(1 for r in results.values() if r.scorecard.medal_tier == "GOLD"),
                "silver_medals": sum(1 for r in results.values() if r.scorecard.medal_tier == "SILVER"),
                "average_score": round(sum(r.scorecard.composite_score for r in results.values()) / len(results), 2),
                "results": {k: v.model_dump() for k, v in results.items()},
            }
        else:
            if payload.role_id not in ALL_ROLES:
                raise HTTPException(status_code=404, detail=f"Role '{payload.role_id}' not found in organization hierarchy.")
            res = training_engine.run_agent_tournament(payload.role_id)
            return res.model_dump()

    @app.get("/training/leaderboard")
    def get_training_leaderboard():
        return training_engine.get_enterprise_leaderboard()

    @app.get("/training/curriculum/{role_id}")
    def get_role_curriculum(role_id: str):
        curr = get_curriculum(role_id)
        if not curr:
            raise HTTPException(status_code=404, detail=f"Curriculum for role '{role_id}' not found.")
        return curr.model_dump()

    @app.get("/training/curricula")
    def list_all_curricula():
        all_c = get_all_curricula()
        return [
            {
                "role_id": c.role_id,
                "role_title": c.role_title,
                "department": c.department,
                "level": c.level,
                "theorems_count": len(c.theoretical_foundations),
                "formulas_count": len(c.mathematical_formulations),
                "papers_count": len(c.landmark_papers),
                "standards_count": len(c.regulatory_and_industry_standards),
                "scenarios_count": len(c.benchmark_scenarios),
            }
            for c in all_c.values()
        ]

    return app

app = create_app()
