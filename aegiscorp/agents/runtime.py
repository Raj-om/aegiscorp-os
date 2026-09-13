import json
import time
import uuid
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.org.graph import AuthorityGraph
from aegiscorp.governance.policy import PolicyEngine, PolicyEvaluationResult
from aegiscorp.governance.risk import RiskEngine, RiskAssessment
from aegiscorp.governance.approval import ApprovalService, ApprovalStatus
from aegiscorp.agents.llm import LLMAdapter, get_llm_adapter
from aegiscorp.agents.prompts import PromptFactory
from aegiscorp.company.db import DatabaseManager
from aegiscorp.company.state import get_default_company_state

class AgentTurnRequest(BaseModel):
    agent_id: str
    role_id: str
    objective: str
    task: str
    capital_amount: float = 0.0
    is_legal_contract: bool = False
    involves_external_api: bool = False
    is_production_change: bool = False
    is_ma_transaction: bool = False
    requested_tool: Optional[str] = None
    tool_arguments: Optional[Dict[str, Any]] = None

class AgentTurnResponse(BaseModel):
    turn_id: str
    agent_id: str
    role_id: str
    status: str  # COMPLETED, APPROVAL_REQUIRED, BLOCKED, ESCALATED
    structured_output: Dict[str, Any]
    authority_passed: bool
    policy_evaluation: PolicyEvaluationResult
    risk_assessment: RiskAssessment
    approval_request_id: Optional[str] = None
    tool_executed: bool = False
    tool_result: Optional[Any] = None
    audit_event_id: str
    timestamp: float = Field(default_factory=time.time)

class AgentRuntime:
    """Policy-aware agent runtime enforcing Section 14 ten-stage lifecycle."""

    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        policy_engine: Optional[PolicyEngine] = None,
        risk_engine: Optional[RiskEngine] = None,
        approval_service: Optional[ApprovalService] = None,
        llm_adapter: Optional[LLMAdapter] = None,
    ):
        self.db = db_manager or DatabaseManager()
        self.policy_engine = policy_engine or PolicyEngine()
        self.risk_engine = risk_engine or RiskEngine()
        self.approval_service = approval_service or ApprovalService()
        self.llm = llm_adapter or get_llm_adapter()
        self.graph = AuthorityGraph()

    def execute_turn(self, req: AgentTurnRequest) -> AgentTurnResponse:
        turn_id = f"turn_{uuid.uuid4().hex[:10]}"
        role = ALL_ROLES.get(req.role_id)
        if not role:
            raise ValueError(f"Unknown role_id: {req.role_id}")

        # 1. Context builder & Role policy loader
        state = get_default_company_state()
        state_summary = f"Cash: ${state.finance.cash_and_liquidity:,.0f}, ARR: ${state.finance.annual_run_rate_revenue:,.0f}, Runway: {state.finance.cash_runway_months:.1f}mo"
        policy_summary = "Enforce spending thresholds: $1M (CFO), $10M (CFO+CEO), $100M (Board). No unauthorized commitments."

        # 2. Memory retrieval (mocked/queried from db)
        recent_events = self.db.get_events(limit=5)

        # 3. Task planner / Prompt construction
        sys_prompt = PromptFactory.build_system_prompt(role)
        turn_prompt = PromptFactory.build_turn_prompt(
            role=role,
            objective=req.objective,
            task=req.task,
            company_state_summary=state_summary,
            policies_summary=policy_summary,
        )

        # 4. LLM Generation
        raw_llm_output = self.llm.generate(sys_prompt, turn_prompt)

        # 5. Structured output validator
        try:
            structured_data = json.loads(raw_llm_output)
        except Exception:
            structured_data = {
                "situation_assessment": raw_llm_output[:200],
                "recommendation": "Execution proposed.",
                "raw_text": raw_llm_output,
            }

        # 6. Authority check (Deterministic)
        authority_passed = self.graph.is_authorized_action(
            role_id=req.role_id,
            action_name=req.requested_tool or "general_action",
            capital_amount=req.capital_amount,
        )

        # 7. Risk check
        risk_eval = self.risk_engine.assess(
            capital_amount=req.capital_amount,
            available_cash=state.finance.cash_and_liquidity,
            is_legal_contract=req.is_legal_contract,
            involves_external_api=req.involves_external_api,
            is_production_change=req.is_production_change,
            is_ma_transaction=req.is_ma_transaction,
            proposer_level=role.level,
        )

        # 8. Policy & Approval evaluation
        policy_eval = self.policy_engine.evaluate_decision(
            proposer_role_id=req.role_id,
            action_type=req.requested_tool or "general_action",
            capital_amount=req.capital_amount,
            risk_score=risk_eval.composite_score,
            is_ma=req.is_ma_transaction,
        )

        approval_req_id = None
        status = "COMPLETED"

        if not authority_passed:
            status = "BLOCKED"
            structured_data["escalation_reason"] = f"Action exceeds {role.title} authority or capital limit (${role.approval_limits.max_capital_commitment:,.0f})."

        if policy_eval.requires_approval:
            status = "APPROVAL_REQUIRED"
            app_req = self.approval_service.create_request(
                decision_id=turn_id,
                decision_content=json.dumps(structured_data),
                requester_role_id=req.role_id,
                required_approvers=policy_eval.required_approvers,
                summary=f"{role.title} requests {req.task} with capital allocation of ${req.capital_amount:,.2f}",
                capital_amount=req.capital_amount,
            )
            approval_req_id = app_req.id

        # 9. Tool executor (Least privilege via ToolGateway)
        tool_executed = False
        tool_result = None
        if req.requested_tool and status == "COMPLETED":
            from aegiscorp.execution.tools import ToolGateway
            gateway = ToolGateway()
            t_res = gateway.execute_tool(req.role_id, req.requested_tool, req.tool_arguments or {})
            tool_executed = (t_res.status == "SUCCESS")
            tool_result = t_res.output if tool_executed else {"status": "failed", "error": t_res.error_message}

        # 10. Ledger writer (Immutable audit event)
        audit_event_id = f"evt_{uuid.uuid4().hex[:12]}"
        self.db.record_event(
            event_id=audit_event_id,
            event_type="agent_turn_completed",
            aggregate_id=turn_id,
            actor=req.role_id,
            payload={
                "agent_id": req.agent_id,
                "role_id": req.role_id,
                "objective": req.objective,
                "task": req.task,
                "capital_amount": req.capital_amount,
                "status": status,
                "risk_score": risk_eval.composite_score,
                "approval_req_id": approval_req_id,
                "tool_executed": tool_executed,
            },
        )

        return AgentTurnResponse(
            turn_id=turn_id,
            agent_id=req.agent_id,
            role_id=req.role_id,
            status=status,
            structured_output=structured_data,
            authority_passed=authority_passed,
            policy_evaluation=policy_eval,
            risk_assessment=risk_eval,
            approval_request_id=approval_req_id,
            tool_executed=tool_executed,
            tool_result=tool_result,
            audit_event_id=audit_event_id,
        )
