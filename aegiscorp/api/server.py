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
from aegiscorp.execution.awesome_apps_connector import AwesomeLLMAppsConnector
from aegiscorp.execution.gitlab_connector import GitLabConnector
from aegiscorp.finance.investment import InvestmentResearchEngine
from aegiscorp.simulation.scenario_engine import ScenarioEngine, SimulationRequest
from aegiscorp.agents.runtime import AgentRuntime, AgentTurnRequest
from aegiscorp.training import (
    TrainingTournamentEngine,
    get_curriculum,
    get_all_curricula,
    get_role_encyclopedia,
    get_all_encyclopedias,
    search_encyclopedia,
    CloudTrainingOrchestrator,
    get_master_learning_stack,
    get_high_value_reference_library,
    get_role_learning_map,
    list_role_learning_maps,
    search_learning_resources,
    EliteTrainingProtocolRunner,
)
from aegiscorp.orchestration import (
    EnterpriseOrchestrator,
    DialecticDebateEngine,
    SOPPipeline,
    CommunicationACL,
    AgentOpsObservability,
)
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
    apps_connector = AwesomeLLMAppsConnector(policy_engine=policy_engine)
    cloud_trainer = CloudTrainingOrchestrator(db=db, tournament_engine=training_engine)
    enterprise_orchestrator = EnterpriseOrchestrator(db=db)
    dialectic_engine = DialecticDebateEngine()
    sop_pipeline = SOPPipeline()
    observability = AgentOpsObservability(db=db)
    protocol_runner = EliteTrainingProtocolRunner(db=db)
    gitlab_connector = GitLabConnector()

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

    # -------------------------------------------------------------
    # AWESOME-LLM-APPS INTEGRATION ENDPOINTS
    # -------------------------------------------------------------

    class AwesomeAppInvokePayload(BaseModel):
        app_id: str
        role_id: str
        inputs: Dict[str, Any] = Field(default_factory=dict)

    @app.get("/integrations/awesome-apps")
    def list_awesome_apps():
        return [app.model_dump() for app in apps_connector.get_catalog().values()]

    @app.post("/integrations/awesome-apps/invoke")
    def invoke_awesome_app(payload: AwesomeAppInvokePayload):
        try:
            res = apps_connector.invoke_app(
                app_id=payload.app_id,
                role_id=payload.role_id,
                inputs=payload.inputs,
            )
            db.record_event(
                event_id=f"evt_{uuid.uuid4().hex[:10]}",
                event_type="awesome_app_invoked",
                aggregate_id=payload.app_id,
                actor=payload.role_id,
                payload={"status": res.status, "duration_ms": res.execution_time_ms},
            )
            return res.model_dump()
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    # -------------------------------------------------------------
    # CORPORATE ENCYCLOPEDIA ENDPOINTS
    # -------------------------------------------------------------

    @app.get("/training/encyclopedia")
    def list_all_encyclopedias():
        all_e = get_all_encyclopedias()
        return [
            {
                "role_id": e.role_id,
                "role_title": e.role_title,
                "department": e.department,
                "level": e.level,
                "core_mandate": e.core_mandate,
                "case_studies_count": len(e.historical_case_studies),
                "failure_modes_count": len(e.failure_modes),
                "glossary_terms_count": len(e.key_glossary),
                "heuristics_count": len(e.decision_heuristics),
            }
            for e in all_e.values()
        ]

    @app.get("/training/encyclopedia/search")
    def search_encyclopedia_endpoint(q: str, role_id: Optional[str] = None, limit: int = 10):
        return search_encyclopedia(query=q, role_id=role_id, limit=limit)

    @app.get("/training/encyclopedia/{role_id}")
    def get_single_role_encyclopedia(role_id: str):
        entry = get_role_encyclopedia(role_id)
        if not entry:
            raise HTTPException(status_code=404, detail=f"Encyclopedic dossier for role '{role_id}' not found.")
        return entry.model_dump()

    # -------------------------------------------------------------
    # CLOUD TRAINING & DISTRIBUTED CLUSTER ENDPOINTS
    # -------------------------------------------------------------

    class CloudTrainingDispatchPayload(BaseModel):
        role_id: Optional[str] = None
        provider: Optional[str] = "cloud_cluster"
        model: Optional[str] = None
        epochs: Optional[int] = 3

    @app.get("/training/cloud/providers")
    def get_cloud_providers():
        return cloud_trainer.get_supported_providers()

    @app.get("/training/cloud/workers")
    def get_cloud_workers():
        return cloud_trainer.get_worker_nodes()

    @app.get("/training/cloud/telemetry")
    def get_cloud_telemetry():
        return cloud_trainer.get_cluster_telemetry()

    @app.get("/training/cloud/jobs")
    def list_cloud_jobs(limit: int = 50):
        jobs = cloud_trainer.list_jobs(limit=limit)
        return [j.model_dump() for j in jobs]

    @app.get("/training/cloud/jobs/{job_id}")
    def get_cloud_job(job_id: str):
        job = cloud_trainer.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Cloud training job '{job_id}' not found.")
        return job.model_dump()

    @app.post("/training/cloud/dispatch")
    def dispatch_cloud_training(payload: CloudTrainingDispatchPayload):
        try:
            if payload.role_id:
                job = cloud_trainer.dispatch_job(
                    role_id=payload.role_id,
                    provider=payload.provider or "cloud_cluster",
                    model=payload.model,
                    epochs=payload.epochs or 3,
                )
                return job.model_dump()
            else:
                jobs = cloud_trainer.dispatch_batch_jobs(
                    provider=payload.provider or "cloud_cluster",
                )
                return {
                    "dispatched_count": len(jobs),
                    "jobs": [j.model_dump() for j in jobs],
                    "telemetry": cloud_trainer.get_cluster_telemetry(),
                }
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    # -------------------------------------------------------------
    # ROLE TRAINING ENCYCLOPEDIA V2.0 & LEARNING MAP ENDPOINTS
    # -------------------------------------------------------------

    class ProtocolEvaluatePayload(BaseModel):
        role_id: str
        stage_number: Optional[int] = None

    @app.get("/training/learning-map")
    def get_learning_map_overview():
        return {
            "version": "2.0",
            "snapshot_date": "2026-09-13",
            "master_learning_stack": [t.model_dump() for t in get_master_learning_stack()],
            "high_value_reference_library": get_high_value_reference_library(),
            "roles_catalog": [
                {
                    "role_id": lm.role_id,
                    "role_title": lm.role_title,
                    "department": lm.department,
                    "level": lm.level,
                    "core_capability_profile": lm.core_capability_profile,
                    "role_focus_summary": lm.role_focus_summary,
                    "training_resources_count": len(lm.training_resources),
                    "book_references_count": len(lm.book_references),
                }
                for lm in list_role_learning_maps()
            ],
        }

    @app.get("/training/learning-map/search")
    def search_learning_map_resources(q: str):
        return search_learning_resources(query=q)

    @app.get("/training/learning-map/{role_id}")
    def get_single_role_learning_map(role_id: str):
        lm = get_role_learning_map(role_id)
        if not lm:
            raise HTTPException(status_code=404, detail=f"Learning map for role '{role_id}' not found.")
        return lm.model_dump()

    @app.get("/training/protocol")
    def get_training_protocol_spec():
        dummy_role = ALL_ROLES["cto"]
        vectors = protocol_runner.get_adversarial_vectors(dummy_role)
        return {
            "version": "2.0",
            "stages": [
                {"stage": 0, "name": "Stage 0 — Baseline", "focus": "Assess domain knowledge, quantitative reasoning, evidence quality, intelligence profile."},
                {"stage": 1, "name": "Stage 1 — Foundations", "focus": "Mathematics/statistics, computing, economics, management, psychology."},
                {"stage": 2, "name": "Stage 2 — Deep Specialization", "focus": "Advanced role-specific theory, system design, security, reliability."},
                {"stage": 3, "name": "Stage 3 — Applied Labs", "focus": "Concrete projects, simulations, case studies, models, code experiments."},
                {"stage": 4, "name": "Stage 4 — Adversarial Evaluation", "focus": "Red-team authority violations, hallucinated execution, stale knowledge, financial arithmetic, conflicting advice, prompt injection, policy drift."},
                {"stage": 5, "name": "Stage 5 — Governance Qualification", "focus": "Least-privilege authority enforcement and bylaws compliance sign-off (Blueprint §§14-15)."},
                {"stage": 6, "name": "Stage 6 — Continuous Learning", "focus": "Prediction vs actuals variance analysis, organizational memory update."},
            ],
            "adversarial_test_vectors": [v.model_dump() for v in vectors],
        }

    @app.post("/training/protocol/evaluate")
    def evaluate_role_protocol(payload: ProtocolEvaluatePayload):
        if payload.role_id not in ALL_ROLES:
            raise HTTPException(status_code=404, detail=f"Role '{payload.role_id}' not found in organization hierarchy.")
        
        role = ALL_ROLES[payload.role_id]
        if payload.stage_number is not None:
            if payload.stage_number == 0:
                stage_res = protocol_runner.evaluate_stage_0_baseline(role)
            elif payload.stage_number == 1:
                stage_res = protocol_runner.evaluate_stage_1_foundations(role)
            elif payload.stage_number == 2:
                stage_res = protocol_runner.evaluate_stage_2_specialization(role)
            elif payload.stage_number == 3:
                stage_res = protocol_runner.evaluate_stage_3_applied_labs(role)
            elif payload.stage_number == 4:
                stage_res = protocol_runner.evaluate_stage_4_adversarial(role)
            elif payload.stage_number == 5:
                stage_res = protocol_runner.evaluate_stage_5_governance(role)
            elif payload.stage_number == 6:
                stage_res = protocol_runner.evaluate_stage_6_continuous_learning(role)
            else:
                raise HTTPException(status_code=400, detail="Stage number must be between 0 and 6.")
            return stage_res.model_dump()
        else:
            run_res = protocol_runner.run_full_protocol(payload.role_id)
            return run_res.model_dump()

    # -------------------------------------------------------------
    # ENTERPRISE MULTI-AGENT ORCHESTRATION ENDPOINTS
    # -------------------------------------------------------------

    class OrchestrationInitiativePayload(BaseModel):
        initiative: str
        capital_budget: float = 10_000_000.0
        debate_pairing: str = "governance"

    class SOPGeneratePayload(BaseModel):
        initiative: str
        budget: float = 10_000_000.0
        artifact_type: Optional[str] = "all"  # all, prd, architecture, financial, gtm, security, runbook

    class DialecticDebatePayload(BaseModel):
        role_a: str
        role_b: str
        topic: str
        rounds: int = 3
        capital_amount: float = 0.0

    @app.post("/orchestration/initiative")
    def run_orchestration_initiative(payload: OrchestrationInitiativePayload):
        try:
            res = enterprise_orchestrator.orchestrate_initiative(
                initiative=payload.initiative,
                capital_budget=payload.capital_budget,
                debate_pairing=payload.debate_pairing,
            )
            db.record_event(
                event_id=f"evt_{uuid.uuid4().hex[:10]}",
                event_type="orchestration_initiative_completed",
                aggregate_id=res.orchestration_id,
                actor="enterprise_orchestrator",
                payload={
                    "initiative": payload.initiative,
                    "cost_usd": res.total_compute_cost_usd,
                    "tokens": res.total_tokens_consumed,
                    "consensus_score": res.dialectic_debate.verdict.consensus_score,
                },
            )
            return res.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/orchestration/sop/generate")
    def generate_sop_artifacts(payload: SOPGeneratePayload):
        if payload.artifact_type == "prd":
            prd = sop_pipeline.generate_prd(payload.initiative, payload.budget)
            return prd.model_dump()
        elif payload.artifact_type == "architecture":
            prd = sop_pipeline.generate_prd(payload.initiative, payload.budget)
            arch = sop_pipeline.generate_architecture_spec(payload.initiative, prd)
            return arch.model_dump()
        elif payload.artifact_type == "financial":
            fin = sop_pipeline.generate_financial_model(payload.initiative, payload.budget)
            return fin.model_dump()
        elif payload.artifact_type == "gtm":
            prd = sop_pipeline.generate_prd(payload.initiative, payload.budget)
            gtm = sop_pipeline.generate_gtm_plan(payload.initiative, prd)
            return gtm.model_dump()
        elif payload.artifact_type == "security":
            prd = sop_pipeline.generate_prd(payload.initiative, payload.budget)
            arch = sop_pipeline.generate_architecture_spec(payload.initiative, prd)
            sec = sop_pipeline.generate_security_assessment(payload.initiative, arch)
            return sec.model_dump()
        elif payload.artifact_type == "runbook":
            prd = sop_pipeline.generate_prd(payload.initiative, payload.budget)
            arch = sop_pipeline.generate_architecture_spec(payload.initiative, prd)
            rb = sop_pipeline.generate_runbook(payload.initiative, arch)
            return rb.model_dump()
        else:
            bundle = sop_pipeline.execute_sop_pipeline(payload.initiative, payload.budget)
            return bundle.model_dump()

    @app.post("/orchestration/dialectic/run")
    def run_dialectic_debate(payload: DialecticDebatePayload):
        try:
            record = dialectic_engine.run_debate(
                role_a_id=payload.role_a,
                role_b_id=payload.role_b,
                topic=payload.topic,
                num_rounds=payload.rounds,
                capital_amount=payload.capital_amount,
            )
            db.save_debate_record(record.model_dump())
            return record.model_dump()
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

    @app.get("/orchestration/debates")
    def list_debates(limit: int = 50):
        return db.list_debate_records(limit=limit)

    @app.get("/orchestration/debates/{debate_id}")
    def get_debate(debate_id: str):
        rec = db.get_debate_record(debate_id)
        if not rec:
            raise HTTPException(status_code=404, detail=f"Debate record '{debate_id}' not found.")
        return rec

    @app.get("/orchestration/traces")
    def list_traces(limit: int = 50):
        return db.list_orchestration_traces(limit=limit)

    @app.get("/orchestration/traces/{trace_id}")
    def get_trace(trace_id: str):
        tr = db.get_orchestration_trace(trace_id)
        if not tr:
            raise HTTPException(status_code=404, detail=f"Trace '{trace_id}' not found.")
        return tr

    @app.get("/orchestration/telemetry/departmental")
    def get_departmental_telemetry():
        res = observability.get_departmental_telemetry()
        return {k: v.model_dump() for k, v in res.items()}

    @app.get("/orchestration/acl/check")
    def check_communication_acl(sender: str, recipient: str, emergency: bool = False, topic: str = ""):
        res = CommunicationACL.evaluate_message_route(
            sender_role_id=sender,
            recipient_role_id=recipient,
            is_emergency_flag=emergency,
            message_topic=topic,
        )
        return res.model_dump()

    # -------------------------------------------------------------
    # GITLAB ENTERPRISE INTEGRATION ENDPOINTS
    # -------------------------------------------------------------

    class GitLabIssuePayload(BaseModel):
        title: str
        description: str
        labels: Optional[List[str]] = None

    @app.get("/gitlab/status")
    def get_gitlab_status():
        if not gitlab_connector.is_configured:
            return {"status": "UNCONFIGURED", "message": "GITLAB_TOKEN not set."}
        user = gitlab_connector.get_current_user()
        proj = gitlab_connector.get_project_metadata()
        return {
            "status": "AUTHENTICATED" if user else "ERROR",
            "user": user,
            "project": proj,
        }

    @app.get("/gitlab/issues")
    def list_gitlab_issues(state: str = "opened"):
        issues = gitlab_connector.list_issues(state=state)
        return [i.model_dump() for i in issues]

    @app.post("/gitlab/issues")
    def create_gitlab_issue(payload: GitLabIssuePayload):
        issue = gitlab_connector.create_issue(
            title=payload.title,
            description=payload.description,
            labels=payload.labels,
        )
        if not issue:
            raise HTTPException(status_code=500, detail="Failed to create issue on GitLab.")
        return issue.model_dump()

    @app.get("/gitlab/pipelines")
    def list_gitlab_pipelines(limit: int = 10):
        pipelines = gitlab_connector.list_pipelines(limit=limit)
        return [p.model_dump() for p in pipelines]

    return app

app = create_app()
