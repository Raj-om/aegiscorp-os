import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class FinancialState(BaseModel):
    cash_and_liquidity: float = 85_000_000.0  # $85M liquid reserves
    annual_run_rate_revenue: float = 120_000_000.0  # $120M ARR
    gross_margin_percent: float = 78.5
    monthly_burn_rate: float = 2_800_000.0
    cash_runway_months: float = 30.3
    operating_reserve: float = 35_000_000.0
    growth_capital_budget: float = 30_000_000.0
    rnd_innovation_budget: float = 12_000_000.0
    market_portfolio_value: float = 8_000_000.0
    market_portfolio_cash: float = 8_000_000.0

class WorkforceState(BaseModel):
    headcount: int = 420
    engineering_headcount: int = 180
    product_headcount: int = 45
    sales_headcount: int = 95
    marketing_headcount: int = 35
    operations_headcount: int = 35
    people_headcount: int = 15
    finance_headcount: int = 15
    open_requisitions: int = 24
    critical_skill_coverage_pct: float = 91.5
    turnover_annual_pct: float = 6.2

class CustomerPipeline(BaseModel):
    total_active_customers: int = 850
    enterprise_tier_customers: int = 140
    pipeline_total_value: float = 48_500_000.0
    pipeline_weighted_value: float = 26_200_000.0
    net_retention_rate_pct: float = 128.0
    average_contract_value: float = 142_000.0

class TechnologyState(BaseModel):
    system_availability_pct: float = 99.98
    active_incidents_count: int = 0
    deployment_frequency_per_week: float = 38.0
    lead_time_for_changes_hours: float = 14.5
    change_failure_rate_pct: float = 1.2
    active_clusters_count: int = 18

class RiskRegisterItem(BaseModel):
    id: str
    category: str  # financial, security, compliance, operational, strategic
    title: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    owner: str
    mitigation_plan: str
    status: str = "active"

class CompanyDigitalTwinState(BaseModel):
    """The master corporate digital twin state covering all domains from Section 10."""
    id: str = "state_current"
    company_name: str = "AegisCorp International"
    valuation_estimate: float = 1_850_000_000.0  # $1.85B base valuation
    target_aspiration_valuation: float = 1_000_000_000_000.0  # $1 Trillion
    updated_at: float = Field(default_factory=time.time)
    version: int = 1

    finance: FinancialState = Field(default_factory=FinancialState)
    workforce: WorkforceState = Field(default_factory=WorkforceState)
    sales: CustomerPipeline = Field(default_factory=CustomerPipeline)
    tech: TechnologyState = Field(default_factory=TechnologyState)
    
    strategic_objectives: List[str] = Field(default_factory=lambda: [
        "Scale autonomous cyber defense platform to Fortune 500",
        "Achieve $250M ARR within 18 months with >80% gross margins",
        "Maintain zero-trust governance and deterministic policy enforcement",
        "Expand investment thesis for long-term compound capital growth",
    ])
    
    risk_register: List[RiskRegisterItem] = Field(default_factory=lambda: [
        RiskRegisterItem(
            id="RSK-001",
            category="security",
            title="External Agent Model Drift & Prompt Injection Surface",
            severity="MEDIUM",
            owner="cto",
            mitigation_plan="Deterministic policy engine pre-clears all tool execution and binds approval tokens",
        ),
        RiskRegisterItem(
            id="RSK-002",
            category="financial",
            title="Macro Liquidity Drawdown & Capital Cost Volatility",
            severity="LOW",
            owner="cfo",
            mitigation_plan="Segregate $35M core operating reserve, maintain minimum 24-month runway",
        ),
        RiskRegisterItem(
            id="RSK-003",
            category="operational",
            title="Distributed Cross-Department Dependency Bottlenecks",
            severity="MEDIUM",
            owner="coo",
            mitigation_plan="Autonomous execution graphs with explicit blockers, SLAs, and escalation triggers",
        ),
    ])

    board_resolutions: List[str] = Field(default_factory=lambda: [
        "Resolution 2026-01: Approved Master Governance Protocol and Authority Graph",
        "Resolution 2026-02: Authorized Capital Allocation Limits and CFO Operating Reserve",
        "Resolution 2026-03: Mandated Multi-Trillion-Dollar Evidence-Based Strategy Directive",
    ])

def get_default_company_state() -> CompanyDigitalTwinState:
    return CompanyDigitalTwinState()
