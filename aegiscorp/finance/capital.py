from typing import Dict
from pydantic import BaseModel, Field

class CapitalBucketAllocation(BaseModel):
    operating_reserve: float
    core_growth: float
    innovation_rnd: float
    strategic_investments: float
    market_portfolio: float
    total_capital: float

class CapitalAllocationEngine:
    """Implements Section 28.7 Capital Allocation Policy owned by the CFO."""

    # Target default ratios
    RATIOS = {
        "operating_reserve": 0.40,      # 40% - Payroll, infrastructure, contractual obligations
        "core_growth": 0.35,            # 35% - Product, engineering, GTM expansion
        "innovation_rnd": 0.12,         # 12% - High-upside controlled R&D experiments
        "strategic_investments": 0.08,  # 8% - Strategic partnerships/M&A
        "market_portfolio": 0.05,       # 5% - Liquid public equities paper/risk-bounded portfolio
    }

    def allocate(self, total_liquid_capital: float) -> CapitalBucketAllocation:
        if total_liquid_capital < 10_000_000.0:
            # Protect operating reserve first if liquid capital is low
            res = total_liquid_capital * 0.80
            growth = total_liquid_capital * 0.20
            return CapitalBucketAllocation(
                operating_reserve=res,
                core_growth=growth,
                innovation_rnd=0.0,
                strategic_investments=0.0,
                market_portfolio=0.0,
                total_capital=total_liquid_capital,
            )

        return CapitalBucketAllocation(
            operating_reserve=round(total_liquid_capital * self.RATIOS["operating_reserve"], 2),
            core_growth=round(total_liquid_capital * self.RATIOS["core_growth"], 2),
            innovation_rnd=round(total_liquid_capital * self.RATIOS["innovation_rnd"], 2),
            strategic_investments=round(total_liquid_capital * self.RATIOS["strategic_investments"], 2),
            market_portfolio=round(total_liquid_capital * self.RATIOS["market_portfolio"], 2),
            total_capital=total_liquid_capital,
        )
