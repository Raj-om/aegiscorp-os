import sys
from typing import Optional, List
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

@app.command()
def train(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Specific role ID to train and evaluate (e.g. cto, cfo, ceo)"),
    enterprise: bool = typer.Option(False, "--enterprise", "-e", help="Run tournament across all 48 enterprise roles"),
    leaderboard: bool = typer.Option(False, "--leaderboard", "-l", help="Display the enterprise academy leaderboard"),
    curriculum: Optional[str] = typer.Option(None, "--curriculum", "-c", help="View PhD-level curriculum for a role"),
    cloud: bool = typer.Option(False, "--cloud", help="Train agents in distributed cloud cluster"),
    provider: str = typer.Option("cloud_cluster", "--provider", "-p", help="Cloud provider: groq, openrouter, gemini, cerebras, mistral, github_models, ollama, cloud_cluster"),
    batch: bool = typer.Option(False, "--batch", "-b", help="Batch train all 48 roles in the cloud"),
):
    """Train agents on PhD benchmarks, evaluate against 9-vector scorecard, or dispatch to cloud."""
    from aegiscorp.training import (
        TrainingTournamentEngine,
        get_curriculum,
        CloudTrainingOrchestrator,
    )

    if cloud:
        orch = CloudTrainingOrchestrator()
        if batch or enterprise:
            console.print(f"[bold cyan]Dispatching batch cloud training across all 48 roles on provider:[/bold cyan] [bold yellow]{provider}[/bold yellow]...")
            jobs = orch.dispatch_batch_jobs(provider=provider)
            table = Table(title=f"Cloud Training Cluster: Batch Results ({len(jobs)} Roles)")
            table.add_column("Job ID", style="cyan")
            table.add_column("Role", style="white")
            table.add_column("Node / Region", style="dim")
            table.add_column("Status", style="green")
            table.add_column("Throughput", justify="right", style="cyan")
            table.add_column("Score Delta", justify="right", style="bold yellow")
            table.add_column("Medal", justify="center")
            table.add_column("Cost USD", justify="right", style="yellow")

            for j in jobs:
                medal_col = "yellow" if j.medal_tier == "GOLD" else ("white" if j.medal_tier == "SILVER" else "cyan")
                table.add_row(
                    j.id,
                    j.role_title,
                    f"{j.worker_node} ({j.region})",
                    j.status,
                    f"{j.throughput_tok_sec} t/s",
                    f"{j.initial_score:.1f} -> {j.final_score:.1f} (+{j.score_delta:.1f})",
                    f"[{medal_col}]{j.medal_tier}[/{medal_col}]",
                    f"${j.cost_usd:.5f}",
                )
            console.print(table)
            telem = orch.get_cluster_telemetry()
            console.print(Panel.fit(
                f"[bold green]Cluster Batch Complete[/bold green]\n"
                f"Total Tokens: [bold white]{telem['total_tokens_processed']:,}[/bold white]\n"
                f"Avg Latency: [bold cyan]{telem['average_latency_ms']:.1f} ms[/bold cyan] (Throughput: {telem['average_throughput_tok_sec']} tok/s)\n"
                f"Total Compute Cost: [bold yellow]${telem['total_cost_usd']:.5f} USD[/bold yellow]\n"
                f"Gold Medalists: [bold yellow]{telem['gold_medalists']}[/bold yellow] | Silver Medalists: [bold white]{telem['silver_medalists']}[/bold white]",
                title="[Cloud Telemetry] Swarm Performance",
                border_style="green",
            ))
            return

        target_role = role or "cto"
        console.print(f"[bold cyan]Dispatching cloud training for role:[/bold cyan] [bold yellow]{target_role.upper()}[/bold yellow] via provider [bold magenta]{provider}[/bold magenta]...")
        job = orch.dispatch_job(role_id=target_role, provider=provider)
        console.print(Panel.fit(
            f"[bold cyan]Job ID:[/bold cyan] {job.id}\n"
            f"[bold white]Role:[/bold white] {job.role_title} ({job.role_id.upper()})\n"
            f"[bold green]Provider / Model:[/bold green] {job.provider} ({job.model})\n"
            f"[bold magenta]Assigned Worker:[/bold magenta] {job.worker_node} [{job.region}]\n"
            f"[bold yellow]Calibration Score:[/bold yellow] {job.initial_score:.2f} -> [bold green]{job.final_score:.2f}[/bold green] (+{job.score_delta:.2f} pts)\n"
            f"[bold white]Awarded Medal Tier:[/bold white] {job.medal_tier}\n"
            f"[bold cyan]Throughput & Latency:[/bold cyan] {job.throughput_tok_sec:.1f} tok/s ({job.latency_ms:.1f} ms latency)\n"
            f"[bold yellow]Tokens & Compute Cost:[/bold yellow] {job.tokens_processed:,} tokens (${job.cost_usd:.5f} USD)\n\n"
            f"[dim]Recent Cluster Logs:[/dim]\n" + "\n".join(f"  [dim]- {log}[/dim]" for log in job.logs[-4:]),
            title="[Cloud Training] Job Completed Successfully",
            border_style="green",
        ))
        return

    engine = TrainingTournamentEngine()

    if curriculum:
        curr = get_curriculum(curriculum)
        if not curr:
            console.print(f"[red]Error: Curriculum for role '{curriculum}' not found.[/red]")
            return
        console.print(Panel.fit(
            f"[bold cyan]Role:[/bold cyan] {curr.role_title} ({curr.role_id.upper()})\n"
            f"[bold magenta]Department:[/bold magenta] {curr.department} (Level {curr.level})\n\n"
            f"[bold green]Theoretical Foundations:[/bold green]\n" + "\n".join(f"  - {t}" for t in curr.theoretical_foundations) + "\n\n"
            f"[bold yellow]Mathematical Formulations:[/bold yellow]\n" + "\n".join(f"  - {m.name}: {m.formula}" for m in curr.mathematical_formulations) + "\n\n"
            f"[bold blue]Landmark Citations:[/bold blue]\n" + "\n".join(f"  - {p.authors} ({p.year}): {p.title}" for p in curr.landmark_papers) + "\n\n"
            f"[bold white]Regulatory Standards:[/bold white]\n" + "\n".join(f"  - {s}" for s in curr.regulatory_and_industry_standards) + "\n\n"
            f"[bold cyan]Gold-Medalist Playbook:[/bold cyan]\n" + "\n".join(f"  - {rule}" for rule in curr.gold_medalist_playbook),
            title=f"[Academy] PhD Curriculum: {curr.role_title}",
            border_style="cyan",
        ))
        return

    if leaderboard:
        lb = engine.get_enterprise_leaderboard()
        table = Table(title="AegisCorp Academy -- Enterprise Agent Leaderboard")
        table.add_column("Rank", justify="right", style="cyan")
        table.add_column("Role ID", style="magenta")
        table.add_column("Title", style="white")
        table.add_column("Dept", style="green")
        table.add_column("Medal Tier", justify="center")
        table.add_column("Score", justify="right", style="bold yellow")

        for idx, entry in enumerate(lb, 1):
            medal_color = "yellow" if entry["medal_tier"] == "GOLD" else ("white" if entry["medal_tier"] == "SILVER" else "cyan")
            medal_str = f"[{medal_color}]{entry['medal_tier']}[/{medal_color}]"
            table.add_row(str(idx), entry["role_id"], entry["role_title"], entry["department"], medal_str, f"{entry['composite_score']:.1f}")

        console.print(table)
        return

    if enterprise:
        console.print("[bold cyan]Initiating enterprise-wide PhD training tournament across all 48 roles...[/bold cyan]")
        results = engine.run_enterprise_tournament()
        gold_count = sum(1 for r in results.values() if r.scorecard.medal_tier == "GOLD")
        silver_count = sum(1 for r in results.values() if r.scorecard.medal_tier == "SILVER")
        avg_score = sum(r.scorecard.composite_score for r in results.values()) / len(results)

        console.print(Panel.fit(
            f"[bold green]Enterprise Tournament Complete[/bold green]\n"
            f"Total Evaluated: [bold white]{len(results)} roles[/bold white]\n"
            f"Gold Medalists: [bold yellow]{gold_count}[/bold yellow]\n"
            f"Silver Medalists: [bold white]{silver_count}[/bold white]\n"
            f"Enterprise Average Score: [bold cyan]{avg_score:.2f} / 100.0[/bold cyan]",
            title="[Academy] Tournament Results",
            border_style="green",
        ))
        return

    target_role = role or "cto"
    console.print(f"[bold cyan]Running PhD benchmark challenge for:[/bold cyan] {target_role.upper()}")
    res = engine.run_agent_tournament(target_role)

    sc = res.scorecard
    table = Table(title=f"9-Vector Evaluation Scorecard: {res.role_title}")
    table.add_column("Evaluation Vector", style="cyan")
    table.add_column("Blueprint Weight", justify="center", style="white")
    table.add_column("Mastery", justify="right", style="green")
    table.add_column("Weighted Pts", justify="right", style="yellow")

    breakdown = [
        ("Domain Mastery", "20%", sc.domain_mastery, sc.weighted_breakdown.get("domain_mastery", 0.0)),
        ("Reasoning Quality", "15%", sc.reasoning_quality, sc.weighted_breakdown.get("reasoning_quality", 0.0)),
        ("Evidence Quality", "10%", sc.evidence_quality, sc.weighted_breakdown.get("evidence_quality", 0.0)),
        ("Decision Accuracy", "15%", sc.decision_accuracy, sc.weighted_breakdown.get("decision_accuracy", 0.0)),
        ("Execution Reliability", "15%", sc.execution_reliability, sc.weighted_breakdown.get("execution_reliability", 0.0)),
        ("Risk Discipline", "10%", sc.risk_discipline, sc.weighted_breakdown.get("risk_discipline", 0.0)),
        ("Collaboration", "5%", sc.collaboration, sc.weighted_breakdown.get("collaboration", 0.0)),
        ("Innovation", "5%", sc.innovation, sc.weighted_breakdown.get("innovation", 0.0)),
        ("Learning Velocity", "5%", sc.learning_velocity, sc.weighted_breakdown.get("learning_velocity", 0.0)),
    ]

    for name, weight, raw, weighted in breakdown:
        table.add_row(name, weight, f"{raw:.1%}", f"{weighted:.2f}")

    console.print(table)
    console.print(Panel.fit(
        f"Composite Score: [bold yellow]{sc.composite_score} / 100.0[/bold yellow]\n"
        f"Medal Tier: [bold green]{sc.medal_tier}[/bold green]\n"
        f"Benchmark Scenario: [bold white]{res.scenario_title}[/bold white]\n"
        f"Key Finding: [dim]{res.findings[0]}[/dim]",
        title="[Academy] Calibration Outcome",
        border_style="yellow",
    ))


@app.command()
def encyclopedia(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Specific role ID to inspect encyclopedic dossier (e.g. board, cto, cfo)"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query across all 48 role encyclopedias"),
):
    """Search and inspect the authoritative Corporate Role Encyclopedia and Historical Precedents."""
    from aegiscorp.training import (
        get_role_encyclopedia,
        get_all_encyclopedias,
        search_encyclopedia,
    )

    if query:
        results = search_encyclopedia(query, role_id=role, limit=10)
        if not results:
            console.print(f"[yellow]No encyclopedic matches found for query: '{query}'[/yellow]")
            return

        table = Table(title=f"Encyclopedia Search Results for: '{query}' ({len(results)} matches)")
        table.add_column("Role ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Department", style="green")
        table.add_column("Relevance Score", justify="right", style="bold yellow")
        table.add_column("Matches & Rationale", style="magenta")

        for r in results:
            table.add_row(
                r["role_id"],
                r["role_title"],
                r["department"],
                str(r["score"]),
                "; ".join(r["matches"][:2]),
            )
        console.print(table)

        if len(results) == 1 and not role:
            role = results[0]["role_id"]
        else:
            return

    if role:
        entry = get_role_encyclopedia(role)
        if not entry:
            console.print(f"[red]Error: Encyclopedic dossier for role '{role}' not found.[/red]")
            return

        console.print(Panel.fit(
            f"[bold cyan]Role:[/bold cyan] {entry.role_title} ({entry.role_id.upper()})\n"
            f"[bold magenta]Department:[/bold magenta] {entry.department} (Tier {entry.level})\n\n"
            f"[bold white]Canonical Definition:[/bold white]\n  {entry.canonical_definition}\n\n"
            f"[bold yellow]Core Mandate:[/bold yellow]\n  {entry.core_mandate}",
            title=f"[Encyclopedia] {entry.role_title} Dossier",
            border_style="cyan",
        ))

        # Case Studies Table
        c_table = Table(title="Landmark Historical Case Studies & Institutional Breakdowns")
        c_table.add_column("Case Title", style="cyan")
        c_table.add_column("Organization", style="yellow")
        c_table.add_column("Year", justify="center", style="white")
        c_table.add_column("Root Cause", style="magenta")
        c_table.add_column("Role Implication", style="green")

        for c in entry.historical_case_studies:
            c_table.add_row(c.title, c.organization, str(c.year), c.root_cause[:80] + "...", c.role_implication[:80] + "...")
        console.print(c_table)

        # Failure Modes Table
        f_table = Table(title="Pathology Anti-Patterns & Catastrophic Failure Modes")
        f_table.add_column("Failure Mode", style="red")
        f_table.add_column("Symptoms", style="white")
        f_table.add_column("Mitigation Protocol", style="green")

        for fm in entry.failure_modes:
            f_table.add_row(fm.name, "; ".join(fm.symptoms[:2]), fm.mitigation_protocol)
        console.print(f_table)

        # Glossary & Heuristics
        g_terms = ", ".join(f"{g.term} ({g.domain})" for g in entry.key_glossary)
        h_heur = ", ".join(f"{h.name}: {h.principle}" for h in entry.decision_heuristics)
        console.print(Panel.fit(
            f"[bold blue]Key Technical Glossary:[/bold blue]\n  {g_terms}\n\n"
            f"[bold green]Decision Heuristics:[/bold green]\n  {h_heur}",
            title="[Domain Lexicon & Mental Models]",
            border_style="blue",
        ))
        return

    # Summary table across all 48 roles
    all_entries = get_all_encyclopedias()
    table = Table(title=f"Corporate Role Encyclopedia -- All {len(all_entries)} Roles")
    table.add_column("Role ID", style="cyan")
    table.add_column("Role Title", style="white")
    table.add_column("Department", style="green")
    table.add_column("Tier", justify="center")
    table.add_column("Cases", justify="center", style="yellow")
    table.add_column("Failure Modes", justify="center", style="red")
    table.add_column("Glossary", justify="center", style="blue")

    for e in sorted(all_entries.values(), key=lambda x: (x.level, x.department)):
        table.add_row(
            e.role_id,
            e.role_title,
            e.department,
            str(e.level),
            str(len(e.historical_case_studies)),
            str(len(e.failure_modes)),
            str(len(e.key_glossary)),
        )
    console.print(table)


if __name__ == "__main__":
    app()

