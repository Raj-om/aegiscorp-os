import pytest
from aegiscorp.governance.policy import PolicyEngine
from aegiscorp.governance.approval import ApprovalService, ApprovalStatus
from aegiscorp.governance.risk import RiskEngine

def test_capital_threshold_tier1():
    """Commitment >= $1M requires CFO review."""
    engine = PolicyEngine()
    result = engine.evaluate_decision("vp_eng", "capital_commitment", capital_amount=2_500_000.0)
    assert result.requires_approval
    assert "cfo" in result.required_approvers
    assert "POL_CAPITAL_TIER1" in result.triggered_policies

def test_capital_threshold_tier2():
    """Commitment >= $10M requires CFO and CEO review."""
    engine = PolicyEngine()
    result = engine.evaluate_decision("cfo", "capital_commitment", capital_amount=15_000_000.0)
    assert result.requires_approval
    assert "cfo" in result.required_approvers
    assert "ceo" in result.required_approvers
    assert "POL_CAPITAL_TIER2" in result.triggered_policies

def test_capital_threshold_tier3():
    """Commitment >= $100M requires CFO, CEO, and Board review."""
    engine = PolicyEngine()
    result = engine.evaluate_decision("ceo", "capital_commitment", capital_amount=120_000_000.0)
    assert result.requires_approval
    assert "cfo" in result.required_approvers
    assert "ceo" in result.required_approvers
    assert "board" in result.required_approvers
    assert "POL_CAPITAL_TIER3" in result.triggered_policies

def test_structural_ma_requires_board():
    """M&A or structural changes always require Board review."""
    engine = PolicyEngine()
    result = engine.evaluate_decision("ceo", "m_and_a", is_ma=True)
    assert result.requires_approval
    assert "board" in result.required_approvers
    assert "POL_STRUCTURAL_MA" in result.triggered_policies

def test_critical_risk_trigger():
    """Critical risk score (>=80) triggers Board & Executive review."""
    engine = PolicyEngine()
    result = engine.evaluate_decision("cto", "general_action", risk_score=85.0)
    assert result.requires_approval
    assert "board" in result.required_approvers
    assert "ceo" in result.required_approvers

def test_approval_token_cryptographic_binding():
    """Verify approval token is cryptographically bound to exact decision version."""
    service = ApprovalService()
    req = service.create_request(
        decision_id="dec_123",
        decision_content='{"objective": "Cloud infrastructure expansion", "amount": 2500000}',
        requester_role_id="vp_eng",
        required_approvers=["cfo"],
        summary="Expand GPU clusters",
        capital_amount=2500000.0,
    )

    assert req.status == ApprovalStatus.PENDING
    assert not service.is_fully_approved(req.id)

    # Approve
    service.record_approval(req.id, "cfo", True, "Approved per quarterly capital plan.")
    assert service.is_fully_approved(req.id)

    # Verify token
    token = req.approvals["cfo"].token
    assert service.verify_token(req.id, "cfo", token)
    # Tampered token fails
    assert not service.verify_token(req.id, "cfo", "forged_token_123")

def test_unauthorized_approver_rejected():
    """Verify unauthorized role cannot record an approval."""
    service = ApprovalService()
    req = service.create_request(
        decision_id="dec_999",
        decision_content="content",
        requester_role_id="vp_eng",
        required_approvers=["cfo"],
        summary="Test",
    )

    with pytest.raises(PermissionError):
        service.record_approval(req.id, "junior_eng", True, "Attempted unauthorized approval")
