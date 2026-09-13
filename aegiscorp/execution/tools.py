import hashlib
import time
import uuid
from typing import Dict, Any, Optional, List, Callable
from pydantic import BaseModel, Field

class ToolExecutionResult(BaseModel):
    tool_name: str
    arguments_hash: str
    status: str  # SUCCESS, REJECTED_UNAUTHORIZED, FAILED
    output: Optional[Any] = None
    error_message: Optional[str] = None
    execution_duration_ms: float = 0.0
    audit_id: str

class ToolGateway:
    """Tool execution gateway enforcing least privilege and per-role tool allowlists."""

    # Explicit allowlists mapping role to allowed tool primitives
    ROLE_TOOL_PERMISSIONS = {
        "board": ["read_audit_ledger", "view_financial_state", "view_kpi_tower"],
        "ceo": ["read_audit_ledger", "view_financial_state", "view_kpi_tower", "broadcast_executive_directive", "run_simulation"],
        "cfo": ["read_audit_ledger", "view_financial_state", "view_kpi_tower", "simulate_capital_allocation", "run_paper_trade", "run_simulation"],
        "coo": ["read_audit_ledger", "view_kpi_tower", "query_capacity", "run_simulation"],
        "cto": ["read_audit_ledger", "view_kpi_tower", "code_review_scan", "query_telemetry", "run_simulation"],
        "cmo": ["view_kpi_tower", "search_web_research", "query_market_trends"],
        "cro": ["view_kpi_tower", "query_pipeline_metrics", "generate_commercial_quote"],
        "chro": ["view_kpi_tower", "query_workforce_capacity", "publish_requisition"],
        "cpo": ["view_kpi_tower", "query_feature_adoption", "generate_roadmap_spec"],
        
        # Engineering Ladder
        "vp_eng": ["code_review_scan", "query_telemetry", "view_kpi_tower"],
        "director_eng": ["code_review_scan", "query_telemetry"],
        "sr_eng_mgr": ["code_review_scan", "query_telemetry"],
        "eng_mgr": ["code_review_scan", "run_linter"],
        "tech_lead": ["code_review_scan", "run_linter", "run_unit_tests"],
        "sr_swe": ["run_linter", "run_unit_tests", "execute_code_sandbox"],
        "swe": ["run_linter", "run_unit_tests", "execute_code_sandbox"],
        "junior_eng": ["run_linter", "run_unit_tests"],

        # Default for research/analysis roles
        "default": ["search_web_research", "read_local_doc", "view_kpi_tower"],
    }

    def __init__(self):
        self._handlers: Dict[str, Callable] = {
            "search_web_research": self._handle_web_search,
            "read_audit_ledger": self._handle_read_ledger,
            "run_unit_tests": self._handle_unit_tests,
            "run_paper_trade": self._handle_paper_trade,
            "simulate_capital_allocation": self._handle_capital_allocation,
            "view_kpi_tower": self._handle_view_kpi,
            "view_financial_state": self._handle_view_financials,
        }

    def is_tool_allowed(self, role_id: str, tool_name: str) -> bool:
        allowed = self.ROLE_TOOL_PERMISSIONS.get(role_id, self.ROLE_TOOL_PERMISSIONS["default"])
        return (tool_name in allowed) or ("*" in allowed)

    def execute_tool(self, role_id: str, tool_name: str, arguments: Dict[str, Any]) -> ToolExecutionResult:
        start = time.time()
        arg_str = str(sorted(arguments.items()))
        arg_hash = hashlib.sha256(arg_str.encode("utf-8")).hexdigest()[:16]
        audit_id = f"tool_run_{uuid.uuid4().hex[:10]}"

        # 1. Verify least privilege allowlist
        if not self.is_tool_allowed(role_id, tool_name):
            return ToolExecutionResult(
                tool_name=tool_name,
                arguments_hash=arg_hash,
                status="REJECTED_UNAUTHORIZED",
                error_message=f"Role '{role_id}' is not authorized to execute tool '{tool_name}'. Action stopped at gateway.",
                audit_id=audit_id,
            )

        # 2. Execute approved tool handler
        handler = self._handlers.get(tool_name)
        if not handler:
            # Fallback simulated tool execution
            output = {"result": f"Executed tool '{tool_name}' successfully", "params": arguments}
        else:
            output = handler(arguments)

        duration = (time.time() - start) * 1000.0

        return ToolExecutionResult(
            tool_name=tool_name,
            arguments_hash=arg_hash,
            status="SUCCESS",
            output=output,
            execution_duration_ms=round(duration, 2),
            audit_id=audit_id,
        )

    # Tool implementations
    def _handle_web_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        query = args.get("query", "corporate technology")
        return {
            "source": "Research Engine",
            "query": query,
            "results": [
                {"title": f"Official Architecture Guidelines for {query}", "url": "https://specs.aegiscorp.internal/v1", "relevance": 0.96},
                {"title": f"Benchmarking {query} in Production", "url": "https://research.aegiscorp.internal/benchmarks", "relevance": 0.91},
            ],
            "retrieved_at": time.time(),
        }

    def _handle_read_ledger(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "info": "Audit ledger stream active and cryptographically verified."}

    def _handle_unit_tests(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "passed", "tests_run": 24, "failed": 0, "coverage_pct": 98.5}

    def _handle_paper_trade(self, args: Dict[str, Any]) -> Dict[str, Any]:
        symbol = args.get("symbol", "INDEX")
        action = args.get("action", "BUY")
        amount = args.get("amount", 100_000.0)
        return {"status": "executed_simulated", "symbol": symbol, "action": action, "amount": amount, "timestamp": time.time()}

    def _handle_capital_allocation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "modeled", "operating_reserve_healthy": True, "projected_roi": 0.28}

    def _handle_view_kpi(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "retrieved", "kpis": {"availability": 99.98, "runway_months": 30.3, "arr": 120_000_000.0}}

    def _handle_view_financials(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "retrieved", "cash": 85_000_000.0, "monthly_burn": 2_800_000.0}
