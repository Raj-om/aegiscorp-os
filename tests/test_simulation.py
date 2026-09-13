import pytest
from aegiscorp.simulation.scenario_engine import ScenarioEngine, SimulationRequest
from aegiscorp.finance.capital import CapitalAllocationEngine
from aegiscorp.finance.investment import InvestmentResearchEngine
from aegiscorp.strategy.scenarios import MultiTrillionAspirationModel

def test_scenario_monte_carlo_engine():
    """Verify Monte Carlo simulation outputs 10/50/90 percentiles and runway projections."""
    engine = ScenarioEngine()
    req = SimulationRequest(
        strategic_objective="Global enterprise expansion",
        capital_budget=20_000_000.0,
        hiring_target=40,
        monte_carlo_iterations=200,
    )
    result = engine.run_simulation(req)

    assert result.mode.startswith("SIMULATION")
    assert result.monte_carlo.p50_arr > 0
    assert result.monte_carlo.p10_arr <= result.monte_carlo.p50_arr <= result.monte_carlo.p90_arr
    assert "cfo" in result.approval_requirements
    assert "base_case" in result.scenario_branches

def test_capital_allocation_buckets():
    """Verify capital is partitioned according to Section 28.7 CFO policy."""
    allocator = CapitalAllocationEngine()
    allocation = allocator.allocate(50_000_000.0)

    # Operating reserve (40%) = $20M
    assert allocation.operating_reserve == 20_000_000.0
    # Core growth (35%) = $17.5M
    assert allocation.core_growth == 17_500_000.0
    # Innovation R&D (12%) = $6.0M
    assert allocation.innovation_rnd == 6_000_000.0
    # Total ties out
    assert allocation.total_capital == 50_000_000.0

def test_public_equities_paper_trading_simulator():
    """Verify paper trading executes within segregated portfolio limits without touching operating reserves."""
    engine = InvestmentResearchEngine()
    thesis = engine.formulate_thesis("GOOGL", current_price=175.0)

    assert thesis.symbol == "GOOGL"
    assert thesis.target_price > 175.0
    assert thesis.expected_return_pct > 0

    order = engine.execute_paper_trade(
        symbol="GOOGL",
        action="BUY",
        amount_usd=250_000.0,
        current_price=175.0,
    )

    assert order.status == "FILLED"
    assert order.execution_mode == "SIMULATED_PAPER"
    assert "GOOGL" in engine.positions

    summary = engine.get_portfolio_summary()
    assert summary["total_portfolio_value"] > 0
    assert summary["cash_balance"] < 3_452_000.0

def test_multi_trillion_strategic_horizons():
    """Verify 1, 3, 5, and 10 year targets from Section 28.5."""
    horizons = MultiTrillionAspirationModel.get_strategic_horizons()

    assert "1_year" in horizons
    assert "3_year" in horizons
    assert "5_year" in horizons
    assert "10_year" in horizons

    assert horizons["1_year"].target_arr == 250_000_000.0
    assert horizons["10_year"].target_enterprise_valuation == 1_000_000_000_000.0
