from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class AuthorityScope(str, Enum):
    GOVERNANCE = "governance"
    STRATEGY = "strategy"
    FINANCE = "finance"
    OPERATIONS = "operations"
    TECHNOLOGY = "technology"
    PRODUCT = "product"
    SALES = "sales"
    MARKETING = "marketing"
    PEOPLE = "people"
    RESEARCH = "research"
    EXECUTION = "execution"

class ApprovalLimits(BaseModel):
    max_capital_commitment: float = 0.0  # Max USD authorized without superior approval
    can_hire: bool = False
    can_fire: bool = False
    can_commit_legal: bool = False
    can_execute_market_trades: bool = False
    requires_board_approval: bool = False

class IntelligenceProfile(BaseModel):
    domain_expertise_score: float = 0.95
    reasoning_confidence: float = 0.90
    evidence_quality_score: float = 0.88
    uncertainty_estimate: float = 0.15
    creativity_score: float = 0.85
    execution_reliability: float = 0.92
    historical_forecast_accuracy: float = 0.86
    risk_discipline: float = 0.95
    cross_functional_literacy: float = 0.88
    learning_velocity: float = 0.90

class Role(BaseModel):
    role_id: str
    title: str
    level: int  # 0=Board, 1=CEO, 2=C-Suite, 3=VP, 4=Director, 5=Manager/Lead, 6=IC
    reports_to: Optional[str] = None
    department: str
    authority: List[str]
    approval_limits: ApprovalLimits
    responsibilities: List[str]
    objectives: List[str] = Field(default_factory=list)
    kpis: List[str] = Field(default_factory=list)
    escalation_targets: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    elite_domain_mastery: List[str] = Field(default_factory=list)

class Agent(BaseModel):
    id: str
    role_id: str
    name: str
    status: str = "active"  # active, idle, deliberating, executing, suspended
    model_profile: str = "deterministic"
    intelligence_profile: IntelligenceProfile = Field(default_factory=IntelligenceProfile)
    current_task_id: Optional[str] = None
    last_active_at: Optional[str] = None

class DepartmentLadder(BaseModel):
    name: str
    executive_role_id: str
    ladder_role_ids: List[str]
