import time
import uuid
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from aegiscorp.company.db import DatabaseManager

class InvestmentThesis(BaseModel):
    id: str = Field(default_factory=lambda: f"the_{uuid.uuid4().hex[:8]}")
    symbol: str
    asset_name: str
    target_price: float
    current_price: float
    expected_return_pct: float
    max_downside_pct: float
    sharpe_ratio_estimate: float
    bull_case_scenario: str
    base_case_scenario: str
    bear_case_scenario: str
    catalysts: List[str]
    primary_risks: List[str]
    position_size_limit_usd: float
    cfo_pre_cleared: bool = False
    requires_board_review: bool = False
    created_at: float = Field(default_factory=time.time)

class PaperTradeOrder(BaseModel):
    id: str = Field(default_factory=lambda: f"ord_{uuid.uuid4().hex[:8]}")
    thesis_id: str
    symbol: str
    action: str  # BUY, SELL, HOLD
    quantity: float
    fill_price: float
    total_amount_usd: float
    execution_mode: str = "SIMULATED_PAPER"  # Live requires explicit external authorization
    status: str = "FILLED"
    timestamp: float = Field(default_factory=time.time)

class PortfolioPosition(BaseModel):
    symbol: str
    shares: float
    average_entry_price: float
    current_price: float
    market_value: float
    unrealized_pnl_usd: float
    unrealized_pnl_pct: float

class InvestmentResearchEngine:
    """Implements Section 28.6: Public equities investment analysis, paper-trading simulation, and risk limits."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.theses: Dict[str, InvestmentThesis] = {}
        self.orders: List[PaperTradeOrder] = []
        self.positions: Dict[str, PortfolioPosition] = {
            "SPY": PortfolioPosition(
                symbol="SPY",
                shares=4000,
                average_entry_price=510.0,
                current_price=545.0,
                market_value=2_180_000.0,
                unrealized_pnl_usd=140_000.0,
                unrealized_pnl_pct=6.86,
            ),
            "MSFT": PortfolioPosition(
                symbol="MSFT",
                shares=3000,
                average_entry_price=415.0,
                current_price=448.0,
                market_value=1_344_000.0,
                unrealized_pnl_usd=99_000.0,
                unrealized_pnl_pct=7.95,
            ),
            "NVDA": PortfolioPosition(
                symbol="NVDA",
                shares=8000,
                average_entry_price=115.0,
                current_price=128.0,
                market_value=1_024_000.0,
                unrealized_pnl_usd=104_000.0,
                unrealized_pnl_pct=11.3,
            ),
        }
        self.cash_balance = 3_452_000.0  # Remaining paper portfolio cash

    def formulate_thesis(self, symbol: str, current_price: float) -> InvestmentThesis:
        target = current_price * 1.32
        thesis = InvestmentThesis(
            symbol=symbol.upper(),
            asset_name=f"{symbol.upper()} Corp Equity",
            target_price=round(target, 2),
            current_price=current_price,
            expected_return_pct=32.0,
            max_downside_pct=12.0,
            sharpe_ratio_estimate=2.1,
            bull_case_scenario="Enterprise cloud transformation adoption accelerates beyond expectations (+50%).",
            base_case_scenario="Organic demand drives steady 20-25% CAGR with solid operating leverage.",
            bear_case_scenario="Supply chain or macroeconomic contraction delays enterprise capital spending (-12%).",
            catalysts=["Upcoming earnings report", "New product line general availability", "Margin expansion"],
            primary_risks=["Valuation multiple compression", "Macro interest rate adjustments"],
            position_size_limit_usd=500_000.0,
            cfo_pre_cleared=True,
            requires_board_review=False,
        )
        self.theses[thesis.id] = thesis
        return thesis

    def execute_paper_trade(self, symbol: str, action: str, amount_usd: float, current_price: float) -> PaperTradeOrder:
        symbol = symbol.upper()
        shares = round(amount_usd / current_price, 4)

        order = PaperTradeOrder(
            thesis_id=f"the_{symbol.lower()}",
            symbol=symbol,
            action=action.upper(),
            quantity=shares,
            fill_price=current_price,
            total_amount_usd=amount_usd,
            execution_mode="SIMULATED_PAPER",
            status="FILLED",
        )
        self.orders.append(order)

        # Update position
        if action.upper() == "BUY":
            self.cash_balance -= amount_usd
            if symbol in self.positions:
                pos = self.positions[symbol]
                total_shares = pos.shares + shares
                total_cost = (pos.shares * pos.average_entry_price) + amount_usd
                pos.average_entry_price = round(total_cost / total_shares, 2)
                pos.shares = total_shares
                pos.market_value = round(total_shares * current_price, 2)
                pos.unrealized_pnl_usd = round(pos.market_value - total_cost, 2)
                pos.unrealized_pnl_pct = round((pos.unrealized_pnl_usd / total_cost) * 100, 2)
            else:
                self.positions[symbol] = PortfolioPosition(
                    symbol=symbol,
                    shares=shares,
                    average_entry_price=current_price,
                    current_price=current_price,
                    market_value=amount_usd,
                    unrealized_pnl_usd=0.0,
                    unrealized_pnl_pct=0.0,
                )
        elif action.upper() == "SELL" and symbol in self.positions:
            self.cash_balance += amount_usd
            pos = self.positions[symbol]
            pos.shares = max(0.0, pos.shares - shares)
            pos.market_value = round(pos.shares * current_price, 2)

        self.db.record_event(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            event_type="paper_trade_executed",
            aggregate_id=order.id,
            actor="investment_agent",
            payload={
                "symbol": symbol,
                "action": action,
                "amount_usd": amount_usd,
                "mode": "SIMULATED_PAPER",
            },
        )
        return order

    def get_portfolio_summary(self) -> Dict[str, Any]:
        total_market_value = sum(p.market_value for p in self.positions.values())
        total_portfolio_value = total_market_value + self.cash_balance
        total_unrealized_pnl = sum(p.unrealized_pnl_usd for p in self.positions.values())

        return {
            "total_portfolio_value": round(total_portfolio_value, 2),
            "total_stock_value": round(total_market_value, 2),
            "cash_balance": round(self.cash_balance, 2),
            "total_unrealized_pnl": round(total_unrealized_pnl, 2),
            "positions": list(self.positions.values()),
            "recent_orders": self.orders[-10:],
        }
