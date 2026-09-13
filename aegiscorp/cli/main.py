import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from aegiscorp.company.state import get_default_company_state
from aegiscorp.company.db import DatabaseManager
from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.strategy.engine import StrategyEngine
from aegiscorp.simulation.scenario_engine import ScenarioEngine, SimulationRequest

app = typer.Typer(help="AegisCorp OS: Governed Multi-Agent Corporate Digital Twin CLI")
console = Console()

@app.command()
def status():
    """Display the corporate digital twin vital metrics."""
    state = get_default_company_state()
    console.print(Panel.fit(
        f"[bold cyan]{state.company_name}[/bold cyan]\n"
        f"Valuation Estimate: [bold green]${state.valuation_estimate/1e9:.2f}B[/bold green]\n"
        f"Aspiration Target: [bold magenta]${state.target_aspiration_valuation/1e12:.1f} Trillion[/bold magenta]\n"
        f"Cash & Liquidity: [bold yellow]${state.finance.cash_and_liquidity/1e6:.1f}M[/bold yellow] (Runway: {state.finance.cash_runway_months:.1f} mo)\n"
        f"Annual Run Rate: [bold blue]${state.finance.annual_run_rate_revenue/1e6:.1f}M ARR[/bold blue] (Gross Margin: {state.finance.gross_margin_percent}%)\n"
        f"Headcount: [bold white]{state.workforce.headcount} FTE[/bold white] (Skill Coverage: {state.workforce.critical_skill_coverage_pct}%)\n"
        f"Platform Availability: [bold green]{state.tech.system_availability_pct}%[/bold green]",
        title="[AegisCorp] Corporate Digital Twin State",
        border_style="cyan"
    ))

@app.command()
def org():
    """List all 39 corporate roles, reporting lines, and delegated spending limits."""
    table = Table(title="AegisCorp OS — 39-Role Corporate Authority Hierarchy")
    table.add_column("Role ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Dept", style="green")
    table.add_column("Reports To", style="magenta")
    table.add_column("Tier", justify="center")
    table.add_column("Cap. Limit", style="yellow")

    for r in sorted(ALL_ROLES.values(), key=lambda x: (x.level, x.department)):
        limit_str = "Unlimited" if r.approval_limits.max_capital_commitment > 1e12 else f"${r.approval_limits.max_capital_commitment:,.0f}"
        table.add_row(r.role_id, r.title, r.department, r.reports_to or "-", str(r.level), limit_str)

    console.print(table)

@app.command(name="run-scenario")
def run_scenario(
    objective: str = typer.Argument("Build a $1B cybersecurity company", help="Strategic objective text"),
    budget: float = typer.Option(25_000_000.0, help="Capital allocation in USD"),
):
    """Decompose a strategic objective into governed departmental workstreams and run simulation."""
    console.print(f"[bold cyan]Initiating Strategic Program for:[/bold cyan] '{objective}' (Budget: ${budget:,.2f})")
    
    strat = StrategyEngine()
    obj = strat.decompose_objective(objective, budget)
    prog = obj.programs[0]

    table = Table(title=f"Strategic Decomposition: {prog.title}")
    table.add_column("Dept", style="green")
    table.add_column("Lead", style="cyan")
    table.add_column("Workstream Objective", style="white")
    table.add_column("Budget", style="yellow")

    for ws in prog.workstreams:
        table.add_row(ws.department, ws.lead_role.upper(), ws.objective, f"${ws.budget:,.2f}")

    console.print(table)

    # Run simulation
    sim_engine = ScenarioEngine()
    sim_res = sim_engine.run_simulation(SimulationRequest(strategic_objective=objective, capital_budget=budget))
    
    console.print(Panel(
        f"[bold green]Median Projected ARR:[/bold green] ${sim_res.monte_carlo.p50_arr/1e6:.1f}M\n"
        f"[bold green]Median Projected Runway:[/bold green] {sim_res.monte_carlo.p50_runway_months} months\n"
        f"[bold yellow]Approval Requirements:[/bold yellow] {', '.join(sim_res.approval_requirements).upper()}\n"
        f"[bold blue]Status:[/bold blue] {sim_res.risk_variance}",
        title="[Monte Carlo] 500-Iteration Forecast",
        border_style="blue"
    ))

@app.command()
def audit(limit: int = typer.Option(10, help="Number of recent events")):
    """View recent immutable audit ledger events."""
    db = DatabaseManager()
    events = db.get_events(limit=limit)
    if not events:
        console.print("[yellow]No audit events recorded yet.[/yellow]")
        return

    table = Table(title=f"Recent Audit Ledger Events (Last {len(events)})")
    table.add_column("Event ID", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Actor", style="magenta")
    table.add_column("Aggregate ID", style="yellow")

    for e in events:
        table.add_row(e["id"], e["type"], e["actor"], e["aggregate_id"])

    console.print(table)

@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host address"),
    port: int = typer.Option(8000, help="Port to bind"),
):
    """Start the AegisCorp OS FastAPI server and Web Control Plane."""
    import uvicorn
    from aegiscorp.api.server import app as fastapi_app

    console.print(f"[bold green]Starting AegisCorp OS Control Plane on http://{host}:{port}[/bold green]")
    uvicorn.run(fastapi_app, host=host, port=port)

if __name__ == "__main__":
    app()
