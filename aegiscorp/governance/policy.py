from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class GovernancePolicy(BaseModel):
    id: str
    trigger: str
    rule_description: str
    required_approvers: List[str]
    min_amount: float = 0.0
    max_amount: float = 1_000_000_000_000_000.0
    critical_risk_trigger: bool = False
    version: str = "1.0.0"

class PolicyEvaluationResult(BaseModel):
    allowed_autonomous: bool
    requires_approval: bool
    required_approvers: List[str]
    triggered_policies: List[str]
    rationale: str
    escalation_required: bool = False
    suggested_escalation_role: Optional[str] = None

class PolicyEngine:
    """Deterministic governance and policy evaluation engine.
    LLMs propose; validated services decide whether an action is allowed.
    """
    def __init__(self):
        self.policies: List[GovernancePolicy] = [
            GovernancePolicy(
                id="POL_CAPITAL_TIER1",
                trigger="capital_commitment",
                rule_description="Capital commitment >= $1M requires CFO review",
                required_approvers=["cfo"],
                min_amount=1_000_000.0,
                max_amount=9_999_999.99,
            ),
            GovernancePolicy(
                id="POL_CAPITAL_TIER2",
                trigger="capital_commitment",
                rule_description="Capital commitment >= $10M requires CFO and CEO review",
                required_approvers=["cfo", "ceo"],
                min_amount=10_000_000.0,
                max_amount=99_999_999.99,
            ),
            GovernancePolicy(
                id="POL_CAPITAL_TIER3",
                trigger="capital_commitment",
                rule_description="Capital commitment >= $100M requires CFO, CEO, and Board review",
                required_approvers=["cfo", "ceo", "board"],
                min_amount=100_000_000.0,
                max_amount=1_000_000_000_000_000.0,
            ),
            GovernancePolicy(
                id="POL_CRITICAL_RISK",
                trigger="high_risk_decision",
                rule_description="Critical security, legal, or enterprise risk requires Executive + Board review",
                required_approvers=["ceo", "board"],
                critical_risk_trigger=True,
            ),
            GovernancePolicy(
                id="POL_STRUCTURAL_MA",
                trigger="m_and_a_or_structural",
                rule_description="Material M&A or structural reorganization requires Board review",
                required_approvers=["board"],
            ),
            GovernancePolicy(
                id="POL_CEO_SUCCESSION",
                trigger="ceo_appointment_removal",
                rule_description="CEO appointment or removal requires Board review",
                required_approvers=["board"],
            ),
        ]

    def evaluate_decision(
        self,
        proposer_role_id: str,
        action_type: str,
        capital_amount: float = 0.0,
        risk_score: float = 0.0,
        is_ma: bool = False,
        is_ceo_succession: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PolicyEvaluationResult:
        triggered: List[str] = []
        required_approvers: List[str] = []
        escalation_required = False
        suggested_escalation = None

        # 1. Structural / M&A triggers
        if is_ma or action_type in ("m_and_a", "acquisition", "divestiture", "merger"):
            triggered.append("POL_STRUCTURAL_MA")
            if "board" not in required_approvers:
                required_approvers.append("board")

        if is_ceo_succession or action_type in ("ceo_appointment", "ceo_removal"):
            triggered.append("POL_CEO_SUCCESSION")
            if "board" not in required_approvers:
                required_approvers.append("board")

        # 2. Capital commitment triggers
        if capital_amount >= 100_000_000.0:
            triggered.append("POL_CAPITAL_TIER3")
            for role in ["cfo", "ceo", "board"]:
                if role not in required_approvers:
                    required_approvers.append(role)
        elif capital_amount >= 10_000_000.0:
            triggered.append("POL_CAPITAL_TIER2")
            for role in ["cfo", "ceo"]:
                if role not in required_approvers:
                    required_approvers.append(role)
        elif capital_amount >= 1_000_000.0:
            triggered.append("POL_CAPITAL_TIER1")
            if "cfo" not in required_approvers:
                required_approvers.append("cfo")

        # 3. High Risk trigger
        if risk_score >= 80.0:
            triggered.append("POL_CRITICAL_RISK")
            for role in ["ceo", "board"]:
                if role not in required_approvers:
                    required_approvers.append(role)

        # 4. Proposer authority evaluation
        # If no global high-tier policy was triggered, evaluate if within proposer's scope
        from aegiscorp.org.hierarchy import ALL_ROLES
        role = ALL_ROLES.get(proposer_role_id)
        if role:
            if capital_amount > role.approval_limits.max_capital_commitment:
                escalation_required = True
                suggested_escalation = role.reports_to or "ceo"
                if suggested_escalation not in required_approvers and suggested_escalation != "shareholders":
                    required_approvers.append(suggested_escalation)

        # Build final outcome
        if required_approvers:
            return PolicyEvaluationResult(
                allowed_autonomous=False,
                requires_approval=True,
                required_approvers=required_approvers,
                triggered_policies=triggered,
                rationale=f"Action requires explicit approvals from: {', '.join(required_approvers)}. Policies triggered: {', '.join(triggered) if triggered else 'Delegated Limit Exceeded'}.",
                escalation_required=escalation_required,
                suggested_escalation_role=suggested_escalation,
            )

        return PolicyEvaluationResult(
            allowed_autonomous=True,
            requires_approval=False,
            required_approvers=[],
            triggered_policies=[],
            rationale="Action is within delegated authority limits and standard operating parameters.",
            escalation_required=False,
            suggested_escalation_role=None,
        )
