import pytest
from fastapi.testclient import TestClient

from aegiscorp.orchestration.sop import (
    SOPPipeline,
    ProductRequirementDocument,
    SystemArchitectureSpec,
    FinancialViabilityModel,
    GoToMarketPlan,
    SecurityComplianceAssessment,
    OperationsRunbook,
    CorporateArtifactBundle,
)
from aegiscorp.orchestration.dialectic import DialecticDebateEngine, DialecticDebateRecord
from aegiscorp.orchestration.mesh import (
    CommunicationACL,
    DynamicTaskDelegator,
    ChannelType,
    ACLCheckResult,
)
from aegiscorp.orchestration.observability import AgentOpsObservability, SpanStatus
from aegiscorp.orchestration.framework import EnterpriseOrchestrator
from aegiscorp.company.db import DatabaseManager
from aegiscorp.api.server import create_app

@pytest.fixture
def db(tmp_path):
    db_file = str(tmp_path / "test_orchestration.db")
    return DatabaseManager(db_path=db_file)

@pytest.fixture
def client(db):
    app = create_app()
    return TestClient(app)

# -------------------------------------------------------------
# 1. MetaGPT SOP & Artifact Tests
# -------------------------------------------------------------

def test_sop_pipeline_generation():
    sop = SOPPipeline()
    bundle = sop.execute_sop_pipeline(initiative="Autonomous Multi-Cloud Core", budget=15_000_000.0)

    assert isinstance(bundle, CorporateArtifactBundle)
    assert bundle.prd is not None
    assert bundle.prd.owner_role == "cpo"
    assert len(bundle.prd.p0_features) >= 3

    assert bundle.architecture_spec is not None
    assert bundle.architecture_spec.owner_role == "cto"
    assert "P99" in bundle.architecture_spec.latency_slos
    assert len(bundle.architecture_spec.c4_containers) >= 4

    assert bundle.financial_model is not None
    assert bundle.financial_model.capital_allocation_usd == 15_000_000.0
    assert bundle.financial_model.hurdle_rate_met is True

    assert bundle.gtm_plan is not None
    assert bundle.gtm_plan.ltv_to_cac_ratio > 3.0

    assert bundle.security_assessment is not None
    assert bundle.security_assessment.audit_approval_status == "APPROVED"

    assert bundle.runbook is not None
    assert len(bundle.runbook.canary_phases) >= 3
    assert bundle.is_fully_signed_off is True

# -------------------------------------------------------------
# 2. ChatDev Dialectic Debate Tests
# -------------------------------------------------------------

def test_dialectic_debate_execution():
    engine = DialecticDebateEngine()
    record = engine.run_debate(
        role_a_id="board",
        role_b_id="ceo",
        topic="High-Risk Global Capital Deployment",
        num_rounds=3,
    )

    assert isinstance(record, DialecticDebateRecord)
    assert record.role_a == "board"
    assert record.role_b == "ceo"
    assert len(record.rounds) == 3

    # Verify ping-pong dialogue structure
    for rnd in record.rounds:
        assert rnd.turn_a.speaker_role_id == "board"
        assert rnd.turn_b.speaker_role_id == "ceo"
        assert len(rnd.turn_a.content) > 20
        assert len(rnd.turn_b.content) > 20

    # Verdict
    assert record.verdict.consensus_score >= 80.0
    assert record.verdict.is_approved is True
    assert len(record.verdict.agreed_compromises) >= 2
    assert len(record.verdict.binding_conditions) >= 1

def test_dialectic_invalid_roles():
    engine = DialecticDebateEngine()
    with pytest.raises(ValueError, match="Invalid debate roles"):
        engine.run_debate("non_existent_role", "ceo", "Some Topic")

# -------------------------------------------------------------
# 3. Agency Swarm Org-Chart ACL Tests
# -------------------------------------------------------------

def test_communication_acl_downstream():
    # CEO (level 1) delegating to CTO (level 2)
    res = CommunicationACL.evaluate_message_route("ceo", "cto")
    assert res.allowed is True
    assert res.channel_type == ChannelType.DOWNSTREAM_DELEGATION
    assert res.audit_flag is False

def test_communication_acl_upstream():
    # CTO (reports to ceo) reporting to CEO
    res = CommunicationACL.evaluate_message_route("cto", "ceo")
    assert res.allowed is True
    assert res.channel_type == ChannelType.UPSTREAM_REPORTING

def test_communication_acl_lateral():
    # CFO (level 2) communicating with CTO (level 2)
    res = CommunicationACL.evaluate_message_route("cfo", "cto")
    assert res.allowed is True
    assert res.channel_type == ChannelType.LATERAL_PEER_SYNC

def test_communication_acl_whistleblower():
    # Junior SWE (level 6) communicating with Board via Whistleblower emergency
    res = CommunicationACL.evaluate_message_route("junior_eng", "board", is_emergency_flag=True)
    assert res.allowed is True
    assert res.channel_type == ChannelType.WHISTLEBLOWER_EMERGENCY
    assert res.audit_flag is True

def test_communication_acl_unauthorized_bypass():
    # Junior SWE (level 6) attempting direct message to Board (level 0) without emergency
    res = CommunicationACL.evaluate_message_route("junior_eng", "board", is_emergency_flag=False)
    assert res.allowed is False
    assert res.channel_type == ChannelType.UNAUTHORIZED_BYPASS
    assert res.audit_flag is True

# -------------------------------------------------------------
# 4. CrewAI Dynamic Skill-Based Delegation Tests
# -------------------------------------------------------------

def test_dynamic_task_delegation(db):
    delegator = DynamicTaskDelegator(db=db)
    candidate = delegator.find_best_agent(
        task_title="Core Distributed Consensus Implementation",
        department="Engineering",
        required_min_tier="SILVER",
    )
    assert candidate is not None
    assert candidate.department == "Engineering"
    assert candidate.is_recommended is True
    assert candidate.composite_score >= 80.0

# -------------------------------------------------------------
# 5. AgentOps Observability & Spans Tests
# -------------------------------------------------------------

def test_agent_ops_trace_and_spans(db):
    obs = AgentOpsObservability(db=db)
    trace = obs.start_trace("Enterprise Cloud Migration")
    assert trace.status == "RUNNING"

    span = obs.create_span(
        trace_id=trace.trace_id,
        name="Security_Audit_Phase",
        role_id="ciso",
        department="Executive",
    )
    assert span.name == "Security_Audit_Phase"

    finished = obs.finish_span(
        trace_id=trace.trace_id,
        span_id=span.span_id,
        tokens_prompt=1500,
        tokens_completion=800,
        status=SpanStatus.OK,
    )
    assert finished is not None
    assert finished.cost_usd > 0.0
    assert finished.duration_ms > 0.0

    completed = obs.complete_trace(trace.trace_id)
    assert completed.status == "COMPLETED"
    assert completed.total_tokens == 2300
    assert completed.total_cost_usd > 0.0

def test_departmental_telemetry(db):
    obs = AgentOpsObservability(db=db)
    stats = obs.get_departmental_telemetry()
    assert "Engineering" in stats
    assert "Executive" in stats
    assert stats["Engineering"].total_spend_usd > 0.0
    assert stats["Engineering"].p99_latency_ms < 150.0

# -------------------------------------------------------------
# 6. Database Persistence Tests
# -------------------------------------------------------------

def test_database_orchestration_persistence(db):
    # Traces
    trace_data = {
        "trace_id": "trc_test123",
        "initiative": "Test Strategic Initiative",
        "status": "COMPLETED",
        "total_cost_usd": 0.045,
        "total_tokens": 15000,
        "duration_ms": 125.0,
        "spans": [{"name": "span_1", "duration_ms": 50.0}],
    }
    db.save_orchestration_trace(trace_data)
    fetched_tr = db.get_orchestration_trace("trc_test123")
    assert fetched_tr is not None
    assert fetched_tr["initiative"] == "Test Strategic Initiative"
    assert fetched_tr["total_tokens"] == 15000

    # Debates
    debate_data = {
        "debate_id": "dbt_test123",
        "topic": "Test Debate Topic",
        "role_a": "cfo",
        "role_b": "cro",
        "verdict": {"consensus_score": 92.0, "is_approved": True},
        "rounds": [],
    }
    db.save_debate_record(debate_data)
    fetched_deb = db.get_debate_record("dbt_test123")
    assert fetched_deb is not None
    assert fetched_deb["consensus_score"] == 92.0

# -------------------------------------------------------------
# 7. Unified Enterprise Orchestrator End-to-End Test
# -------------------------------------------------------------

def test_unified_enterprise_orchestrator(db):
    orch = EnterpriseOrchestrator(db=db)
    result = orch.orchestrate_initiative(
        initiative="Unified Autonomous Multi-Agent Mesh",
        capital_budget=12_000_000.0,
        debate_pairing="governance",
    )

    assert result.status == "COMPLETED"
    assert result.total_tokens_consumed > 5000
    assert result.total_compute_cost_usd > 0.0
    assert result.dialectic_debate.verdict.is_approved is True
    assert result.artifact_bundle.is_fully_signed_off is True
    assert len(result.delegated_assignments) == 4
    assert len(result.acl_validations) == 7

# -------------------------------------------------------------
# 8. REST API Endpoints Tests
# -------------------------------------------------------------

def test_api_orchestration_endpoints(client):
    # 1. Initiative dispatch
    res = client.post(
        "/orchestration/initiative",
        json={"initiative": "API Integration Test Initiative", "capital_budget": 5_000_000.0},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert "orchestration_id" in data

    # 2. SOP Generate
    res = client.post(
        "/orchestration/sop/generate",
        json={"initiative": "API SOP Test", "artifact_type": "prd"},
    )
    assert res.status_code == 200
    assert res.json()["owner_role"] == "cpo"

    # 3. Dialectic Debate
    res = client.post(
        "/orchestration/dialectic/run",
        json={"role_a": "cpo", "role_b": "cto", "topic": "API Gateway Architecture", "rounds": 2},
    )
    assert res.status_code == 200
    assert res.json()["verdict"]["is_approved"] is True

    # 4. Telemetry Departmental
    res = client.get("/orchestration/telemetry/departmental")
    assert res.status_code == 200
    assert "Engineering" in res.json()

    # 5. ACL Check
    res = client.get("/orchestration/acl/check?sender=junior_eng&recipient=board&emergency=true")
    assert res.status_code == 200
    assert res.json()["allowed"] is True
    assert res.json()["channel_type"] == "whistleblower_emergency"
