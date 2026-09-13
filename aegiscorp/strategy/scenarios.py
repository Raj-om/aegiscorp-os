from typing import Dict, List, Any
from pydantic import BaseModel, Field

class HorizonTarget(BaseModel):
    horizon_years: int
    target_arr: float
    target_enterprise_valuation: float
    projected_headcount: int
    required_capital_investment: float
    base_case_probability: float = 0.60
    upside_case_valuation: float
    downside_case_valuation: float
    core_milestones: List[str]
    strategic_risks: List[str]

class MultiTrillionAspirationModel:
    """Models multi-trillion-dollar valuation as a long-term strategic aspiration with base/upside/downside scenarios."""

    @classmethod
    def get_strategic_horizons(cls) -> Dict[str, HorizonTarget]:
        return {
            "1_year": HorizonTarget(
                horizon_years=1,
                target_arr=250_000_000.0,  # $250M ARR
                target_enterprise_valuation=3_500_000_000.0,  # $3.5B
                projected_headcount=650,
                required_capital_investment=45_000_000.0,
                upside_case_valuation=5_000_000_000.0,
                downside_case_valuation=2_200_000_000.0,
                core_milestones=[
                    "Scale Autonomous Defense Core across 50 Fortune 100 enterprises",
                    "Achieve GAAP operational profitability",
                    "Establish zero-defect deterministic policy benchmark",
                ],
                strategic_risks=["Enterprise procurement cycle expansion", "Competitive pricing pressure"],
            ),
            "3_year": HorizonTarget(
                horizon_years=3,
                target_arr=1_200_000_000.0,  # $1.2B ARR
                target_enterprise_valuation=20_000_000_000.0,  # $20B
                projected_headcount=1_800,
                required_capital_investment=150_000_000.0,
                upside_case_valuation=32_000_000_000.0,
                downside_case_valuation=12_000_000_000.0,
                core_milestones=[
                    "Launch global multi-tenant governed digital-twin network",
                    "Complete strategic M&A of adjacent security intelligence platforms",
                    "Establish dominant standard in machine-enforceable corporate governance",
                ],
                strategic_risks=["Global regulatory fragmentation", "Key talent retention in core AI research"],
            ),
            "5_year": HorizonTarget(
                horizon_years=5,
                target_arr=6_500_000_000.0,  # $6.5B ARR
                target_enterprise_valuation=120_000_000_000.0,  # $120B
                projected_headcount=5_500,
                required_capital_investment=600_000_000.0,
                upside_case_valuation=180_000_000_000.0,
                downside_case_valuation=75_000_000_000.0,
                core_milestones=[
                    "Full ecosystem monetization with 10,000+ integrated enterprise twins",
                    "Autonomous public market capital allocation yielding top-decile Sharpe ratio",
                    "Global sovereign and cloud enterprise infrastructure integrations",
                ],
                strategic_risks=["Antitrust scrutiny in enterprise AI platforms", "Macroeconomic liquidity shifts"],
            ),
            "10_year": HorizonTarget(
                horizon_years=10,
                target_arr=50_000_000_000.0,  # $50B ARR
                target_enterprise_valuation=1_000_000_000_000.0,  # $1.0 Trillion Aspiration
                projected_headcount=18_000,
                required_capital_investment=3_000_000_000.0,
                upside_case_valuation=1_800_000_000_000.0,
                downside_case_valuation=450_000_000_000.0,
                core_milestones=[
                    "Universal corporate operating system layer powering the global economy",
                    "Defensible multi-sided network effects across capital, talent, and intelligence",
                    "Continuous organizational self-calibration via Monte Carlo digital twin",
                ],
                strategic_risks=["Civilizational scale technological paradigm shifts"],
            ),
        }
