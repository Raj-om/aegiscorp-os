import pytest
from aegiscorp.agents.runtime import AgentRuntime, AgentTurnRequest
from aegiscorp.agents.prompts import PromptFactory
from aegiscorp.agents.deliberation import ExecutiveDeliberationCouncil
from aegiscorp.org.hierarchy import ALL_ROLES

def test_prompt_factory_generation():
    """Verify dynamic prompt generation includes PhD mastery, limits, and reporting."""
    role = ALL_ROLES["cto"]
    sys_prompt = PromptFactory.build_system_prompt(role)

    assert "Chief Technology Officer" in sys_prompt
    assert "Computer science and advanced software architecture" in sys_prompt
    assert "PhD-Level & Gold-Medalist Intelligence Framework" in sys_prompt
    assert "LLMs propose. Governance services validate" in sys_prompt

def test_deliberation_council_retains_perspectives():
    """Verify multi-agent deliberation gathers diverse functional perspectives and CEO synthesis."""
    council = ExecutiveDeliberationCouncil()
    res = council.deliberate(
        objective="Enter enterprise AI security market",
        proposed_plan="Build governed multi-agent digital twin core",
        capital_amount=15_000_000.0,
    )

    assert len(res.perspectives) == 7  # CTO, CFO, CPO, CRO, CMO, COO, CHRO
    assert "ceo" in res.council_members
    assert "CEO Synthesis" in res.ceo_synthesis
    assert "cfo" in res.required_approvals

def test_runtime_turn_lifecycle_within_limits():
    """Verify agent turn executes cleanly through 10 stages within delegated limits."""
    runtime = AgentRuntime()
    req = AgentTurnRequest(
        agent_id="agt_swe_01",
        role_id="swe",
        objective="Implement unit tests for policy engine",
        task="Write pytest coverage for capital thresholds",
        capital_amount=0.0,
        requested_tool="run_unit_tests",
        tool_arguments={},
    )
    resp = runtime.execute_turn(req)

    assert resp.status == "COMPLETED"
    assert resp.authority_passed
    assert resp.tool_executed
    assert resp.tool_result["status"] == "passed"
    assert resp.audit_event_id.startswith("evt_")

def test_runtime_blocks_unauthorized_capital_commitment():
    """Verify that an agent attempting to commit capital beyond its limit is blocked and gated."""
    runtime = AgentRuntime()
    # SWE attempting $5,000,000 capital commitment
    req = AgentTurnRequest(
        agent_id="agt_swe_02",
        role_id="swe",
        objective="Procure third party cluster",
        task="Purchase high performance compute",
        capital_amount=5_000_000.0,
    )
    resp = runtime.execute_turn(req)

    # Authority must fail because SWE limit is $1,000
    assert not resp.authority_passed
    assert resp.status in ("BLOCKED", "APPROVAL_REQUIRED")
    assert resp.approval_request_id is not None
    assert "cfo" in resp.policy_evaluation.required_approvers
