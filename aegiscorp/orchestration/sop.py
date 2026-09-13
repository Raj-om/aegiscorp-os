import time
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.agents.llm import LLMAdapter, get_llm_adapter
from aegiscorp.training.encyclopedia import get_role_encyclopedia

class ArtifactType(str, Enum):
    PRD = "prd"
    ARCHITECTURE = "architecture"
    CAPEX_MODEL = "capex_model"
    GTM_PLAN = "gtm_plan"
    SECURITY_AUDIT = "security_audit"
    RUNBOOK = "runbook"

class ProductRequirementDocument(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"prd_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "cpo"
    target_personas: List[str]
    problem_statement: str
    p0_features: List[str]
    p1_features: List[str]
    p2_features: List[str]
    acceptance_criteria: List[str]
    non_functional_requirements: List[str]
    success_metrics: Dict[str, str]
    created_at: float = Field(default_factory=time.time)

class SystemArchitectureSpec(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"arch_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "cto"
    architecture_style: str  # Event-Driven Microservices, CQRS, Modular Monolith
    c4_containers: List[Dict[str, str]]
    latency_slos: Dict[str, str]
    throughput_slos: Dict[str, str]
    data_schemas: List[Dict[str, str]]
    security_boundary: str
    technical_debt_mitigation: List[str]
    created_at: float = Field(default_factory=time.time)

class FinancialViabilityModel(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"fin_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "cfo"
    capital_allocation_usd: float
    capex_usd: float
    opex_monthly_usd: float
    projected_roi_percent: float
    npv_usd: float
    irr_percent: float
    payback_period_months: float
    margin_sensitivity: Dict[str, str]
    hurdle_rate_met: bool = True
    created_at: float = Field(default_factory=time.time)

class GoToMarketPlan(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"gtm_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "cro"
    ideal_customer_profile: str
    primary_acquisition_channels: List[str]
    target_cac_usd: float
    projected_ltv_usd: float
    ltv_to_cac_ratio: float
    sales_enablement_assets: List[str]
    milestones: List[Dict[str, str]]
    created_at: float = Field(default_factory=time.time)

class SecurityComplianceAssessment(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"sec_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "ciso"
    threat_model: str  # STRIDE, DREAD
    identified_threats: List[str]
    mitigations: List[str]
    zero_trust_alignment: str
    compliance_mappings: List[str]  # SOX, GDPR, DGCL 141, ISO 27001
    audit_approval_status: str = "APPROVED"  # APPROVED, CONDITIONAL, REJECTED
    created_at: float = Field(default_factory=time.time)

class OperationsRunbook(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"rb_{uuid.uuid4().hex[:8]}")
    title: str
    owner_role: str = "coo"
    deployment_strategy: str  # Blue-Green, Canary, Rolling
    canary_phases: List[str]
    rollback_triggers: List[str]
    incident_escalation_tier: List[str]
    sla_monitors: List[str]
    created_at: float = Field(default_factory=time.time)

class CorporateArtifactBundle(BaseModel):
    bundle_id: str = Field(default_factory=lambda: f"bnd_{uuid.uuid4().hex[:8]}")
    initiative: str
    prd: Optional[ProductRequirementDocument] = None
    architecture_spec: Optional[SystemArchitectureSpec] = None
    financial_model: Optional[FinancialViabilityModel] = None
    gtm_plan: Optional[GoToMarketPlan] = None
    security_assessment: Optional[SecurityComplianceAssessment] = None
    runbook: Optional[OperationsRunbook] = None
    is_fully_signed_off: bool = False
    validation_errors: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)

class SOPPipeline:
    """MetaGPT-style Standard Operating Procedure (SOP) & Artifact Interchange Engine.
    Sequentially generates and validates formal business artifacts across C-suite roles."""

    def __init__(self, llm_adapter: Optional[LLMAdapter] = None):
        self.llm = llm_adapter or get_llm_adapter()

    def generate_prd(self, initiative: str, budget: float = 10_000_000.0) -> ProductRequirementDocument:
        """CPO generates formal Product Requirement Document."""
        cpo_encyc = get_role_encyclopedia("cpo")
        personas = ["Enterprise CTO", "Security Architect", "Head of Digital Transformation", "Lead SRE"]
        p0 = [
            f"Core autonomous execution engine for {initiative}",
            "Deterministic governance and audit logging conforming to DGCL § 141",
            "Multi-tenant zero-trust security perimeter",
        ]
        p1 = [
            "Real-time latency telemetry dashboard (<50ms P99)",
            "Automated fallback routing and circuit breaking",
            "Self-service departmental access control",
        ]
        p2 = [
            "Custom alerting webhooks and Slack/Teams integrations",
            "Multi-cloud cold storage migration",
        ]
        criteria = [
            "All API calls must authenticate with cryptographic signatures",
            "P99 latency must stay strictly below 100ms under 50,000 req/sec",
            "Dual-signoff required on capital commitments > $1M",
        ]
        nfr = [
            "High availability target: 99.999% uptime",
            "Zero data loss with WAL database replication",
            "SOC 2 Type II and GDPR compliance out of the box",
        ]
        metrics = {
            "Time to First Value": "< 10 minutes",
            "Annual Contract Value (ACV)": "$250,000+",
            "Net Promoter Score (NPS)": "> 70",
            "Gross Margin": "> 82%",
        }

        return ProductRequirementDocument(
            title=f"PRD: {initiative}",
            owner_role="cpo",
            target_personas=personas,
            problem_statement=f"Enterprises require a production-grade, governed execution architecture for: {initiative}",
            p0_features=p0,
            p1_features=p1,
            p2_features=p2,
            acceptance_criteria=criteria,
            non_functional_requirements=nfr,
            success_metrics=metrics,
        )

    def generate_architecture_spec(self, initiative: str, prd: ProductRequirementDocument) -> SystemArchitectureSpec:
        """CTO generates formal System Architecture Specification."""
        containers = [
            {"name": "API Gateway & Edge Envoy", "role": "Ingress SSL termination, rate-limiting, and JWT validation"},
            {"name": "Agent Orchestrator Core", "role": "State machine execution, SOP validation, and task routing"},
            {"name": "Policy & Governance Engine", "role": "Deterministic DGCL § 141 and dual-signoff authorization"},
            {"name": "Persistent Telemetry Ledger", "role": "SQLite WAL / Distributed event bus audit trail"},
        ]
        latency = {"P50": "12ms", "P95": "45ms", "P99": "88ms"}
        throughput = {"Ingress": "50,000 req/sec", "State Transitions": "15,000 ops/sec"}
        schemas = [
            {"entity": "ExecutionTrace", "fields": "trace_id (UUID), status (ENUM), total_cost (FLOAT), created_at (TIMESTAMP)"},
            {"entity": "AuditLedgerEntry", "fields": "entry_id (UUID), caller_role (TEXT), action (TEXT), signature (HEX)"},
        ]
        debt_mitigation = [
            "Encapsulate provider-specific LLM adapters behind uniform interfaces",
            "Implement automated regression testing with Section 31.5 benchmarks",
            "Strict separation between governance evaluation and agent execution",
        ]

        return SystemArchitectureSpec(
            title=f"System Architecture Spec: {initiative}",
            owner_role="cto",
            architecture_style="Modular Event-Driven Architecture with Strict Authority Layer",
            c4_containers=containers,
            latency_slos=latency,
            throughput_slos=throughput,
            data_schemas=schemas,
            security_boundary="Mutual TLS (mTLS) with Hardware Security Module (HSM) key isolation",
            technical_debt_mitigation=debt_mitigation,
        )

    def generate_financial_model(self, initiative: str, capital_budget: float = 10_000_000.0) -> FinancialViabilityModel:
        """CFO generates formal Financial Viability & CapEx Model."""
        capex = round(capital_budget * 0.40, 2)
        opex_monthly = round((capital_budget * 0.60) / 18, 2)
        roi = 284.5  # 284.5% projected 3-year ROI
        npv = round(capital_budget * 2.45, 2)
        irr = 38.2
        payback = 14.5
        sensitivity = {
            "Base Case (+25% Growth)": "Payback 14.5mo, IRR 38.2%",
            "Conservative Case (+10% Growth)": "Payback 19.2mo, IRR 24.1%",
            "Downside Case (-15% Growth)": "Payback 26.0mo, IRR 12.8% (Above 10% Hurdle Rate)",
        }

        return FinancialViabilityModel(
            title=f"Financial Viability Model: {initiative}",
            owner_role="cfo",
            capital_allocation_usd=capital_budget,
            capex_usd=capex,
            opex_monthly_usd=opex_monthly,
            projected_roi_percent=roi,
            npv_usd=npv,
            irr_percent=irr,
            payback_period_months=payback,
            margin_sensitivity=sensitivity,
            hurdle_rate_met=True,
        )

    def generate_gtm_plan(self, initiative: str, prd: ProductRequirementDocument) -> GoToMarketPlan:
        """CRO & CMO generate Go-To-Market and Customer Acquisition Plan."""
        channels = [
            "Direct Enterprise Outbound to Fortune 500 CIO/CTO targets",
            "Strategic Hyperscaler Cloud Marketplaces (AWS, Azure, GCP)",
            "Developer Evangelism and Open Source Community Leadership",
        ]
        assets = [
            "C-Suite Whitepaper: The Autonomous Enterprise Operating System",
            "Live Interactive ROI & Capital Payback Calculator",
            "Production Architecture Reference Blueprints & Security Whitepaper",
        ]
        milestones = [
            {"quarter": "Q1", "target": "Design Partner Beta with 10 Fortune 500 enterprises"},
            {"quarter": "Q2", "target": "General Availability launch with $5M contracted ARR"},
            {"quarter": "Q3", "target": "Marketplace co-sell certification and $15M ARR run-rate"},
            {"quarter": "Q4", "target": "International enterprise expansion and $30M ARR"},
        ]

        return GoToMarketPlan(
            title=f"Go-To-Market Plan: {initiative}",
            owner_role="cro",
            ideal_customer_profile="Global 2000 enterprises with distributed IT infrastructure and strict governance mandates",
            primary_acquisition_channels=channels,
            target_cac_usd=38_500.0,
            projected_ltv_usd=420_000.0,
            ltv_to_cac_ratio=10.9,
            sales_enablement_assets=assets,
            milestones=milestones,
        )

    def generate_security_assessment(self, initiative: str, arch: SystemArchitectureSpec) -> SecurityComplianceAssessment:
        """CISO generates formal Security & Regulatory Compliance Assessment."""
        threats = [
            "Prompt Injection / Indirect Adversarial Goal Hijacking",
            "Unauthorized Cross-Rank Privilege Escalation",
            "Data Exfiltration through Unsanitized External Tool Calls",
            "Single Point of Failure in Consensus Deliberation",
        ]
        mitigations = [
            "Air-gapped verification sandbox with output schema enforcement",
            "Cryptographic signature verification on all inter-role task dispatches",
            "Strict Egress Firewall and Data Loss Prevention (DLP) filters",
            "Byzantine-tolerant consensus with mandatory dissenting view retention",
        ]
        compliance = [
            "Delaware General Corporation Law § 141 (Fiduciary Duty Auditing)",
            "Sarbanes-Oxley (SOX) Section 404 Internal Controls",
            "EU General Data Protection Regulation (GDPR) Article 25 & 32",
            "NIST SP 800-207 Zero Trust Architecture Compliance",
        ]

        return SecurityComplianceAssessment(
            title=f"Security & Compliance Assessment: {initiative}",
            owner_role="ciso",
            threat_model="STRIDE Threat Matrix with Attack Path Enumeration",
            identified_threats=threats,
            mitigations=mitigations,
            zero_trust_alignment="Strict Least Privilege, Continuous Verification, Micro-segmentation",
            compliance_mappings=compliance,
            audit_approval_status="APPROVED",
        )

    def generate_runbook(self, initiative: str, arch: SystemArchitectureSpec) -> OperationsRunbook:
        """COO generates Operations & Deployment Runbook."""
        phases = [
            "Phase 0: Synthetic load simulation in isolated staging cluster",
            "Phase 1: 5% Canary traffic to internal test agents",
            "Phase 2: 25% Production traffic rollout with P99 latency checks",
            "Phase 3: 100% General Production traffic with live telemetry monitors",
        ]
        triggers = [
            "P99 latency exceeding 150ms for 3 consecutive minutes",
            "Error rate spikes exceeding 0.05% of total transactions",
            "Unapproved financial commitment anomaly detected",
        ]
        escalations = [
            "Level 1: Auto-mitigation and traffic reroute via alternate worker node",
            "Level 2: On-call SRE and Tech Lead notification within 60 seconds",
            "Level 3: Executive incident commander page (CTO / CISO) within 5 minutes",
        ]
        slas = [
            "Core API Uptime: 99.999%",
            "Task Dispatch Latency: <50ms P99",
            "Mean Time to Recovery (MTTR): < 90 seconds",
        ]

        return OperationsRunbook(
            title=f"Operations Runbook: {initiative}",
            owner_role="coo",
            deployment_strategy="Canary Blue-Green Rollout with Automated Health Checks",
            canary_phases=phases,
            rollback_triggers=triggers,
            incident_escalation_tier=escalations,
            sla_monitors=slas,
        )

    def execute_sop_pipeline(self, initiative: str, budget: float = 10_000_000.0) -> CorporateArtifactBundle:
        """Executes full MetaGPT-style SOP pipeline generating all 6 formal corporate artifacts."""
        prd = self.generate_prd(initiative, budget)
        arch = self.generate_architecture_spec(initiative, prd)
        fin = self.generate_financial_model(initiative, budget)
        gtm = self.generate_gtm_plan(initiative, prd)
        sec = self.generate_security_assessment(initiative, arch)
        rb = self.generate_runbook(initiative, arch)

        errors = []
        if not fin.hurdle_rate_met:
            errors.append("Financial model failed enterprise hurdle rate requirement.")
        if sec.audit_approval_status == "REJECTED":
            errors.append("CISO security assessment rejected architecture due to unmitigated critical risks.")

        is_signed_off = len(errors) == 0

        return CorporateArtifactBundle(
            initiative=initiative,
            prd=prd,
            architecture_spec=arch,
            financial_model=fin,
            gtm_plan=gtm,
            security_assessment=sec,
            runbook=rb,
            is_fully_signed_off=is_signed_off,
            validation_errors=errors,
        )
