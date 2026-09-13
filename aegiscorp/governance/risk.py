from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class RiskAssessment(BaseModel):
    financial_risk: float = Field(default=0.0, ge=0.0, le=100.0)
    operational_risk: float = Field(default=0.0, ge=0.0, le=100.0)
    technical_risk: float = Field(default=0.0, ge=0.0, le=100.0)
    legal_risk: float = Field(default=0.0, ge=0.0, le=100.0)
    strategic_risk: float = Field(default=0.0, ge=0.0, le=100.0)
    composite_score: float = Field(default=0.0, ge=0.0, le=100.0)
    severity_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    detected_factors: List[str] = Field(default_factory=list)
    mitigations: List[str] = Field(default_factory=list)

class RiskEngine:
    """Quantitative risk engine evaluating financial, operational, technical, legal, and strategic exposures."""
    
    WEIGHTS = {
        "financial": 0.25,
        "operational": 0.20,
        "technical": 0.20,
        "legal": 0.20,
        "strategic": 0.15,
    }

    def assess(
        self,
        capital_amount: float = 0.0,
        available_cash: float = 50_000_000.0,
        is_legal_contract: bool = False,
        involves_external_api: bool = False,
        is_production_change: bool = False,
        is_ma_transaction: bool = False,
        proposer_level: int = 2,
    ) -> RiskAssessment:
        factors: List[str] = []
        mitigations: List[str] = []

        # 1. Financial Risk
        fin_ratio = (capital_amount / available_cash) if available_cash > 0 else 1.0
        if fin_ratio > 0.5:
            fin_score = 90.0
            factors.append(f"High capital exposure: {fin_ratio*100:.1f}% of liquid cash")
            mitigations.append("Tranche capital release against delivery milestones; require CFO review")
        elif fin_ratio > 0.2:
            fin_score = 60.0
            factors.append(f"Moderate capital exposure: {fin_ratio*100:.1f}% of liquid cash")
            mitigations.append("Verify budget allocation with VP Finance")
        elif capital_amount > 0:
            fin_score = 25.0
        else:
            fin_score = 10.0

        # 2. Operational Risk
        ops_score = 20.0
        if is_production_change:
            ops_score += 40.0
            factors.append("Direct impact on production environment or operating cadence")
            mitigations.append("Implement automated canary deployments and instant rollbacks")
        if proposer_level >= 5:
            ops_score += 15.0
            factors.append("Initiated at managerial/IC level without executive pre-clearance")

        # 3. Technical Risk
        tech_score = 15.0
        if involves_external_api:
            tech_score += 35.0
            factors.append("Third-party external dependency / API integration")
            mitigations.append("Implement circuit breakers, fallback stubs, and secret isolation")
        if is_production_change:
            tech_score += 25.0

        # 4. Legal / Compliance Risk
        legal_score = 10.0
        if is_legal_contract:
            legal_score += 55.0
            factors.append("Binding commercial or legal commitment")
            mitigations.append("Standard terms review; require CRO/Board signature authorization")
        if is_ma_transaction:
            legal_score += 40.0
            factors.append("Mergers & Acquisitions regulatory review requirement")
            mitigations.append("Fiduciary and antitrust legal clearance required")

        # 5. Strategic Risk
        strat_score = 20.0
        if is_ma_transaction:
            strat_score += 60.0
            factors.append("Material strategic re-alignment or company structure shift")
            mitigations.append("Full executive council deliberation and Board sign-off")
        elif capital_amount >= 10_000_000.0:
            strat_score += 40.0

        # Composite score
        composite = (
            fin_score * self.WEIGHTS["financial"]
            + ops_score * self.WEIGHTS["operational"]
            + tech_score * self.WEIGHTS["technical"]
            + legal_score * self.WEIGHTS["legal"]
            + strat_score * self.WEIGHTS["strategic"]
        )

        composite = min(100.0, max(0.0, composite))

        if composite >= 80.0:
            severity = "CRITICAL"
        elif composite >= 55.0:
            severity = "HIGH"
        elif composite >= 30.0:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        return RiskAssessment(
            financial_risk=round(fin_score, 1),
            operational_risk=round(ops_score, 1),
            technical_risk=round(tech_score, 1),
            legal_risk=round(legal_score, 1),
            strategic_risk=round(strat_score, 1),
            composite_score=round(composite, 1),
            severity_level=severity,
            detected_factors=factors,
            mitigations=mitigations,
        )
