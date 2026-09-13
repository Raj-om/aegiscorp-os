import time
import uuid
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from aegiscorp.company.db import DatabaseManager
from aegiscorp.orchestration.sop import SOPPipeline, CorporateArtifactBundle
from aegiscorp.orchestration.dialectic import DialecticDebateEngine, DialecticDebateRecord
from aegiscorp.orchestration.mesh import CommunicationACL, DynamicTaskDelegator, ACLCheckResult, DelegationCandidate
from aegiscorp.orchestration.observability import AgentOpsObservability, ExecutionTrace

class OrchestrationResult(BaseModel):
    orchestration_id: str = Field(default_factory=lambda: f"orc_{uuid.uuid4().hex[:8]}")
    initiative: str
    capital_budget_usd: float
    status: str = "COMPLETED"
    trace: ExecutionTrace
    dialectic_debate: DialecticDebateRecord
    artifact_bundle: CorporateArtifactBundle
    delegated_assignments: List[Dict[str, Any]]
    acl_validations: List[ACLCheckResult]
    total_compute_cost_usd: float
    total_tokens_consumed: int
    created_at: float = Field(default_factory=time.time)

class EnterpriseOrchestrator:
    """Unified Enterprise Multi-Agent Orchestration Framework.
    Synthesizes MetaGPT (SOPs), ChatDev (Dialectics), Agency Swarm (ACL), CrewAI (Delegation), and AgentOps (Observability)."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.sop = SOPPipeline()
        self.dialectic = DialecticDebateEngine()
        self.delegator = DynamicTaskDelegator(db=self.db)
        self.observability = AgentOpsObservability(db=self.db)

    def orchestrate_initiative(
        self,
        initiative: str,
        capital_budget: float = 10_000_000.0,
        debate_pairing: str = "governance",
    ) -> OrchestrationResult:
        # 1. Initialize AgentOps trace
        trace = self.observability.start_trace(initiative=initiative)

        # 2. ACL Verification Span (CEO delegating to C-Suite)
        acl_span = self.observability.create_span(
            trace_id=trace.trace_id,
            name="OrgChart_ACL_Verification",
            role_id="ceo",
            department="Executive",
        )
        acl_results = [
            CommunicationACL.evaluate_message_route("ceo", "cpo"),
            CommunicationACL.evaluate_message_route("ceo", "cto"),
            CommunicationACL.evaluate_message_route("ceo", "cfo"),
            CommunicationACL.evaluate_message_route("ceo", "cro"),
            CommunicationACL.evaluate_message_route("ceo", "cmo"),
            CommunicationACL.evaluate_message_route("ceo", "chro"),
            CommunicationACL.evaluate_message_route("ceo", "coo"),
        ]
        self.observability.finish_span(
            trace_id=trace.trace_id,
            span_id=acl_span.span_id,
            tokens_prompt=450,
            tokens_completion=180,
        )

        # 3. Dialectic Peer-Review Debate Span
        deb_span = self.observability.create_span(
            trace_id=trace.trace_id,
            name="ChatDev_Dialectic_Peer_Review",
            role_id="board",
            department="Governance",
        )
        pair = self.dialectic.CANONICAL_PAIRINGS.get(debate_pairing, ("board", "ceo", "Governance Fiduciary Review"))
        debate_record = self.dialectic.run_debate(
            role_a_id=pair[0],
            role_b_id=pair[1],
            topic=initiative,
            num_rounds=3,
            capital_amount=capital_budget,
        )
        self.observability.finish_span(
            trace_id=trace.trace_id,
            span_id=deb_span.span_id,
            tokens_prompt=2400,
            tokens_completion=1850,
        )

        # 4. MetaGPT SOP & Artifact Interchange Span
        sop_span = self.observability.create_span(
            trace_id=trace.trace_id,
            name="MetaGPT_SOP_Artifact_Interchange",
            role_id="cpo",
            department="Product",
        )
        artifact_bundle = self.sop.execute_sop_pipeline(initiative=initiative, budget=capital_budget)
        self.observability.finish_span(
            trace_id=trace.trace_id,
            span_id=sop_span.span_id,
            tokens_prompt=3200,
            tokens_completion=2600,
        )

        # 5. CrewAI Dynamic Skill-Based Delegation Span
        del_span = self.observability.create_span(
            trace_id=trace.trace_id,
            name="CrewAI_Dynamic_Skill_Delegation",
            role_id="coo",
            department="Operations",
        )
        workstreams = [
            ("Core Architecture Implementation", "Engineering", "GOLD"),
            ("Product Feature Matrix & User Testing", "Product", "SILVER"),
            ("Go-to-Market Enterprise Outbound", "Sales", "SILVER"),
            ("Continuous Canary Infrastructure Rollout", "Operations", "GOLD"),
        ]

        delegated_assignments = []
        for task_name, dept, min_tier in workstreams:
            candidate = self.delegator.find_best_agent(
                task_title=task_name,
                department=dept,
                required_min_tier=min_tier,
            )
            delegated_assignments.append({
                "task": task_name,
                "department": dept,
                "assigned_role_id": candidate.role_id,
                "assigned_role_title": candidate.role_title,
                "medal_tier": candidate.medal_tier,
                "composite_score": candidate.composite_score,
                "qualification_notes": candidate.qualification_notes,
            })

        self.observability.finish_span(
            trace_id=trace.trace_id,
            span_id=del_span.span_id,
            tokens_prompt=1200,
            tokens_completion=750,
        )

        # 6. Complete AgentOps Trace
        completed_trace = self.observability.complete_trace(trace_id=trace.trace_id) or trace

        # 7. Persist to Database if supported
        try:
            self.db.save_debate_record(debate_record.model_dump())
            self.db.save_sop_bundle(artifact_bundle.model_dump())
        except Exception:
            pass

        return OrchestrationResult(
            initiative=initiative,
            capital_budget_usd=capital_budget,
            status="COMPLETED",
            trace=completed_trace,
            dialectic_debate=debate_record,
            artifact_bundle=artifact_bundle,
            delegated_assignments=delegated_assignments,
            acl_validations=acl_results,
            total_compute_cost_usd=completed_trace.total_cost_usd,
            total_tokens_consumed=completed_trace.total_tokens,
        )
