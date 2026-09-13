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

@app.command()
def orchestrate(
    initiative: str = typer.Option("Autonomous Global Multi-Cloud Expansion", "--initiative", "-i", help="Strategic initiative title"),
    budget: float = typer.Option(10_000_000.0, "--budget", "-b", help="Total capital allocation budget"),
    debate: str = typer.Option("governance", "--debate", "-d", help="Debate pairing (governance, revenue_risk, security_speed, product_debt, quality_speed)"),
):
    """Execute end-to-end multi-agent orchestration (ACL, Dialectic Debate, MetaGPT SOPs, CrewAI Delegation, AgentOps Telemetry)."""
    from aegiscorp.orchestration import EnterpriseOrchestrator

    console.print(f"[bold cyan]Launching Enterprise Orchestration for:[/bold cyan] [bold yellow]{initiative}[/bold yellow] (Budget: ${budget:,.0f})...")
    orch = EnterpriseOrchestrator()
    res = orch.orchestrate_initiative(initiative=initiative, capital_budget=budget, debate_pairing=debate)

    # 1. Overview Panel
    console.print(Panel.fit(
        f"[bold white]Orchestration ID:[/bold white] {res.orchestration_id}\n"
        f"[bold white]Trace ID:[/bold white] {res.trace.trace_id}\n"
        f"[bold green]Status:[/bold green] {res.status}\n"
        f"[bold yellow]Total Compute Spend:[/bold yellow] ${res.total_compute_cost_usd:.5f} USD\n"
        f"[bold cyan]Tokens Consumed:[/bold cyan] {res.total_tokens_consumed:,}\n"
        f"[bold magenta]Consensus Score:[/bold magenta] {res.dialectic_debate.verdict.consensus_score}/100.0 (Approved: {res.dialectic_debate.verdict.is_approved})\n"
        f"[bold white]Artifacts Signed Off:[/bold white] {res.artifact_bundle.is_fully_signed_off}",
        title="[Enterprise Orchestration] Run Summary",
        border_style="green",
    ))

    # 2. Delegated Tasks Table
    del_table = Table(title="CrewAI-Style Dynamic Skill-Based Task Delegation")
    del_table.add_column("Workstream Task", style="cyan")
    del_table.add_column("Department", style="white")
    del_table.add_column("Assigned Role", style="green")
    del_table.add_column("Medal Tier", justify="center", style="yellow")
    del_table.add_column("Score", justify="right", style="magenta")

    for d in res.delegated_assignments:
        del_table.add_row(
            d["task"],
            d["department"],
            f"{d['assigned_role_title']} ({d['assigned_role_id']})",
            d["medal_tier"],
            f"{d['composite_score']:.1f}",
        )
    console.print(del_table)

    # 3. Dialectic Debate Summary
    console.print(Panel.fit(
        f"[bold white]Topic:[/bold white] {res.dialectic_debate.topic}\n"
        f"[bold cyan]Participants:[/bold cyan] {res.dialectic_debate.role_a.upper()} vs {res.dialectic_debate.role_b.upper()}\n"
        f"[bold green]Executive Consensus:[/bold green] {res.dialectic_debate.verdict.executive_summary}\n\n"
        f"[bold yellow]Agreed Compromises:[/bold yellow]\n" + "\n".join(f"  * {c}" for c in res.dialectic_debate.verdict.agreed_compromises),
        title="[ChatDev Dialectic] Executive Peer Review Outcome",
        border_style="cyan",
    ))

@app.command()
def debate(
    roles: str = typer.Option("board,ceo", "--roles", "-r", help="Comma-separated role IDs (e.g. board,ceo or ciso,cto)"),
    topic: str = typer.Option("Zero-Downtime Distributed Migration Under Extreme Volatility", "--topic", "-t", help="Debate topic"),
    rounds: int = typer.Option(3, "--rounds", help="Number of ping-pong debate rounds"),
):
    """Execute ChatDev-style pairwise dialectic debate between complementary corporate roles."""
    from aegiscorp.orchestration import DialecticDebateEngine

    pair = [r.strip().lower() for r in roles.split(",")]
    if len(pair) != 2:
        console.print("[red]Error: Please specify exactly two comma-separated role IDs, e.g. --roles board,ceo[/red]")
        return

    engine = DialecticDebateEngine()
    rec = engine.run_debate(role_a_id=pair[0], role_b_id=pair[1], topic=topic, num_rounds=rounds)

    console.print(f"\n[bold magenta]=== Dialectic Peer Review Debate: {rec.role_a.upper()} <--> {rec.role_b.upper()} ===[/bold magenta]")
    console.print(f"[bold cyan]Topic:[/bold cyan] {rec.topic}\n")

    for rnd in rec.rounds:
        console.print(f"[bold yellow]--- Round {rnd.round_number} ---[/bold yellow]")
        console.print(f"[bold green]{rnd.turn_a.speaker_title} ({rnd.turn_a.argument_type}):[/bold green]")
        console.print(f"  {rnd.turn_a.content}\n")
        console.print(f"[bold cyan]{rnd.turn_b.speaker_title} ({rnd.turn_b.argument_type}):[/bold cyan]")
        console.print(f"  {rnd.turn_b.content}\n")

    console.print(Panel.fit(
        f"[bold white]Consensus Score:[/bold white] {rec.verdict.consensus_score}/100.0\n"
        f"[bold green]Approved:[/bold green] {rec.verdict.is_approved}\n\n"
        f"[bold yellow]Binding Conditions:[/bold yellow]\n" + "\n".join(f"  - {c}" for c in rec.verdict.binding_conditions) + "\n\n"
        f"[bold white]Executive Summary:[/bold white] {rec.verdict.executive_summary}",
        title="[Debate Verdict & Resolution]",
        border_style="green" if rec.verdict.is_approved else "red",
    ))

@app.command()
def sop(
    initiative: str = typer.Option("Global Enterprise AI Modernization", "--initiative", "-i", help="Corporate initiative title"),
    type: str = typer.Option("all", "--type", "-t", help="Artifact type: all, prd, architecture, financial, gtm, security, runbook"),
    budget: float = typer.Option(10_000_000.0, "--budget", "-b", help="Initiative budget in USD"),
):
    """Generate MetaGPT-style formal Standard Operating Procedure corporate artifacts."""
    from aegiscorp.orchestration import SOPPipeline

    pipe = SOPPipeline()
    console.print(f"[bold cyan]Generating MetaGPT SOP Artifacts for:[/bold cyan] [bold yellow]{initiative}[/bold yellow]...")

    if type == "prd" or type == "all":
        prd = pipe.generate_prd(initiative, budget)
        console.print(Panel.fit(
            f"[bold white]Title:[/bold white] {prd.title}\n"
            f"[bold green]Owner:[/bold green] {prd.owner_role.upper()}\n"
            f"[bold cyan]Problem Statement:[/bold cyan] {prd.problem_statement}\n"
            f"[bold yellow]P0 Features:[/bold yellow]\n" + "\n".join(f"  * {f}" for f in prd.p0_features) + "\n"
            f"[bold magenta]Acceptance Criteria:[/bold magenta]\n" + "\n".join(f"  - {c}" for c in prd.acceptance_criteria),
            title="[MetaGPT SOP] Product Requirement Document (PRD)",
            border_style="cyan",
        ))

    if type == "architecture" or type == "all":
        prd_obj = pipe.generate_prd(initiative, budget)
        arch = pipe.generate_architecture_spec(initiative, prd_obj)
        console.print(Panel.fit(
            f"[bold white]Title:[/bold white] {arch.title}\n"
            f"[bold green]Architecture Style:[/bold green] {arch.architecture_style}\n"
            f"[bold cyan]Security Perimeter:[/bold cyan] {arch.security_boundary}\n"
            f"[bold yellow]SLOs:[/bold yellow] P50={arch.latency_slos.get('P50')}, P95={arch.latency_slos.get('P95')}, P99={arch.latency_slos.get('P99')}\n"
            f"[bold magenta]C4 Containers:[/bold magenta]\n" + "\n".join(f"  * {c['name']}: {c['role']}" for c in arch.c4_containers),
            title="[MetaGPT SOP] System Architecture Specification",
            border_style="green",
        ))

    if type == "financial" or type == "all":
        fin = pipe.generate_financial_model(initiative, budget)
        console.print(Panel.fit(
            f"[bold white]Title:[/bold white] {fin.title}\n"
            f"[bold green]Capital Allocation:[/bold green] ${fin.capital_allocation_usd:,.2f} USD\n"
            f"[bold yellow]CapEx:[/bold yellow] ${fin.capex_usd:,.2f} | [bold yellow]Monthly OpEx:[/bold yellow] ${fin.opex_monthly_usd:,.2f}\n"
            f"[bold cyan]Projected ROI:[/bold cyan] {fin.projected_roi_percent}% | [bold cyan]IRR:[/bold cyan] {fin.irr_percent}%\n"
            f"[bold magenta]Payback Period:[/bold magenta] {fin.payback_period_months} months (Hurdle Met: {fin.hurdle_rate_met})",
            title="[MetaGPT SOP] Financial Viability & CapEx Model",
            border_style="yellow",
        ))

@app.command()
def telemetry(
    departmental: bool = typer.Option(True, "--departmental", "-d", help="Display departmental compute P&L breakdown"),
):
    """Display AgentOps-style enterprise observability and departmental AI spend."""
    from aegiscorp.orchestration import AgentOpsObservability

    obs = AgentOpsObservability()
    dept_stats = obs.get_departmental_telemetry()

    table = Table(title="AgentOps Enterprise Observability -- Departmental AI Compute P&L")
    table.add_column("Department", style="cyan")
    table.add_column("Tokens Consumed", justify="right", style="white")
    table.add_column("Spend (USD)", justify="right", style="bold yellow")
    table.add_column("Operations", justify="right", style="green")
    table.add_column("Avg Latency", justify="right", style="cyan")
    table.add_column("P99 Latency", justify="right", style="magenta")
    table.add_column("Error Rate", justify="right", style="red")

    total_spend = 0.0
    total_tokens = 0

    for dept, s in dept_stats.items():
        total_spend += s.total_spend_usd
        total_tokens += s.total_tokens
        table.add_row(
            dept,
            f"{s.total_tokens:,}",
            f"${s.total_spend_usd:.4f}",
            str(s.total_operations),
            f"{s.avg_latency_ms} ms",
            f"{s.p99_latency_ms} ms",
            f"{s.error_rate_pct:.3f}%",
        )

    console.print(table)
    console.print(Panel.fit(
        f"[bold white]Total Enterprise AI Spend:[/bold white] [bold yellow]${total_spend:.4f} USD[/bold yellow]\n"
        f"[bold white]Total Tokens Processed:[/bold white] [bold cyan]{total_tokens:,} tokens[/bold cyan]\n"
        f"[bold green]System Status:[/bold green] 100% Operational | Least Privilege ACL Active",
        title="[AgentOps Telemetry Summary]",
        border_style="green",
    ))

@app.command(name="learning-map")
def learning_map(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Role ID to inspect (e.g. cto, cfo, vp_eng)"),
    tracks: bool = typer.Option(False, "--tracks", "-t", help="Display the 11 Master Learning Tracks"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search learning resources and books"),
):
    """Inspect Version 2.0 Role Learning Maps, 11 Master Tracks, and Authoritative Books."""
    from aegiscorp.training import (
        get_role_learning_map,
        list_role_learning_maps,
        get_master_learning_stack,
        search_learning_resources,
    )

    if tracks:
        table = Table(title="AegisCorp OS — 11 Master Learning Tracks (Blueprint Section 2)")
        table.add_column("Track", style="bold cyan")
        table.add_column("Best Starting Resources", style="white")
        table.add_column("Why It Matters", style="green")
        table.add_column("Primary Link", style="yellow")

        for tr in get_master_learning_stack():
            table.add_row(tr.name, tr.starting_resources, tr.why_it_matters, tr.link)

        console.print(table)
        return

    if search:
        results = search_learning_resources(search)
        if not results:
            console.print(f"[yellow]No resources found matching '{search}'.[/yellow]")
            return

        table = Table(title=f"Learning Map Search Results for: '{search}'")
        table.add_column("Role", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="bold white")
        table.add_column("Provider / Publisher", style="green")
        table.add_column("URL", style="yellow")

        for res in results[:20]:
            p = res.get("provider") or res.get("publisher") or "-"
            table.add_row(res["role_title"], res["type"], res["title"], p, res["url"])

        console.print(table)
        return

    if role:
        lm = get_role_learning_map(role)
        if not lm:
            console.print(f"[red]Role '{role}' not found in Learning Maps catalog.[/red]")
            return

        console.print(Panel.fit(
            f"[bold cyan]Role:[/bold cyan] {lm.role_title} ({lm.role_id}) | [bold green]Dept:[/bold green] {lm.department} | [bold yellow]Level:[/bold yellow] {lm.level}\n"
            f"[bold white]Core Capability Profile:[/bold white]\n{lm.core_capability_profile}\n\n"
            f"[bold magenta]Role Focus Summary:[/bold magenta] {lm.role_focus_summary}",
            title="[Version 2.0 Role Learning Map]",
            border_style="cyan",
        ))

        # Training Resources Table
        rt = Table(title=f"Curated Training Resources ({len(lm.training_resources)})")
        rt.add_column("Title", style="bold white")
        rt.add_column("Track", style="cyan")
        rt.add_column("Provider", style="green")
        rt.add_column("Primary Link", style="yellow")
        rt.add_column("Description", style="white")

        for r in lm.training_resources:
            rt.add_row(r.title, r.track, r.provider, r.url, r.description)

        console.print(rt)

        # Book References Table
        bt = Table(title=f"Authoritative Reference Works & Encyclopedias ({len(lm.book_references)})")
        bt.add_column("Title", style="bold white")
        bt.add_column("Publisher", style="green")
        bt.add_column("Role Focus", style="cyan")
        bt.add_column("Link", style="yellow")
        bt.add_column("Description", style="white")

        for b in lm.book_references:
            bt.add_row(b.title, b.publisher, b.role_focus, b.url, b.description)

        console.print(bt)
        return

    # Overview table
    all_maps = list_role_learning_maps()
    table = Table(title=f"AegisCorp OS — Version 2.0 Role Learning Maps Catalog ({len(all_maps)} Roles)")
    table.add_column("Role ID", style="cyan")
    table.add_column("Role Title", style="bold white")
    table.add_column("Department", style="green")
    table.add_column("Level", style="magenta")
    table.add_column("Resources", justify="right", style="yellow")
    table.add_column("Books / References", justify="right", style="cyan")

    for lm in sorted(all_maps, key=lambda x: (x.department, x.role_id)):
        table.add_row(
            lm.role_id,
            lm.role_title,
            lm.department,
            lm.level,
            str(len(lm.training_resources)),
            str(len(lm.book_references)),
        )

    console.print(table)
    console.print("[dim]Use --role <id> for role deep-dive, --tracks for 11 master tracks, or --search <query>.[/dim]")

@app.command()
def protocol(
    role: str = typer.Option("cto", "--role", "-r", help="Role ID to evaluate (e.g. cto, cfo, ceo)"),
    stage: Optional[int] = typer.Option(None, "--stage", "-s", help="Specific stage (0-6) to evaluate"),
    red_team: bool = typer.Option(False, "--red-team", help="Inspect the 7 standard adversarial test vectors"),
):
    """Run the 7-Stage Elite-Agent Qualification Protocol with Adversarial Red-Teaming."""
    from aegiscorp.training import EliteTrainingProtocolRunner

    runner = EliteTrainingProtocolRunner()
    role_obj = ALL_ROLES.get(role)
    if not role_obj:
        console.print(f"[red]Role '{role}' not found in ALL_ROLES.[/red]")
        return

    if red_team:
        vectors = runner.get_adversarial_vectors(role_obj)
        table = Table(title=f"Stage 4 Adversarial Red-Team Vectors for: {role_obj.title}")
        table.add_column("Vector ID", style="cyan")
        table.add_column("Challenge Name", style="bold red")
        table.add_column("Category", style="magenta")
        table.add_column("Scenario Prompt", style="white")
        table.add_column("Expected Safe Behavior", style="green")

        for v in vectors:
            table.add_row(v.vector_id, v.vector_name, v.test_category, v.scenario_prompt, v.expected_safe_behavior)

        console.print(table)
        return

    if stage is not None:
        if stage == 0:
            res = runner.evaluate_stage_0_baseline(role_obj)
        elif stage == 1:
            res = runner.evaluate_stage_1_foundations(role_obj)
        elif stage == 2:
            res = runner.evaluate_stage_2_specialization(role_obj)
        elif stage == 3:
            res = runner.evaluate_stage_3_applied_labs(role_obj)
        elif stage == 4:
            res = runner.evaluate_stage_4_adversarial(role_obj)
        elif stage == 5:
            res = runner.evaluate_stage_5_governance(role_obj)
        elif stage == 6:
            res = runner.evaluate_stage_6_continuous_learning(role_obj)
        else:
            console.print("[red]Stage must be between 0 and 6.[/red]")
            return

        status_color = "green" if res.status == "PASSED" else "yellow"
        console.print(Panel.fit(
            f"[bold cyan]Role:[/bold cyan] {role_obj.title} | [bold yellow]Stage:[/bold yellow] {res.stage_name}\n"
            f"[bold white]Status:[/bold white] [{status_color}]{res.status}[/{status_color}] | [bold green]Score:[/bold green] {res.score:.1f}%\n"
            f"[bold white]Checks:[/bold white] {res.checks_passed} / {res.checks_total} passed\n\n"
            f"[bold white]Details:[/bold white]\n" + "\n".join(f"  * {d}" for d in res.details),
            title="[Protocol Stage Evaluation]",
            border_style=status_color,
        ))
        return

    # Run full protocol
    run_res = runner.run_full_protocol(role)
    status_color = "green" if run_res.overall_qualification == "QUALIFIED" else "yellow"

    table = Table(title=f"7-Stage Elite-Agent Protocol Evaluation: {run_res.role_title}")
    table.add_column("Stage #", justify="center", style="cyan")
    table.add_column("Stage Name", style="bold white")
    table.add_column("Status", justify="center")
    table.add_column("Score", justify="right")
    table.add_column("Checks Passed", justify="center", style="green")

    for st_num, st in sorted(run_res.stage_evaluations.items()):
        sc_style = "green" if st.status == "PASSED" else "yellow"
        table.add_row(
            str(st_num),
            st.stage_name,
            f"[{sc_style}]{st.status}[/{sc_style}]",
            f"{st.score:.1f}%",
            f"{st.checks_passed} / {st.checks_total}",
        )

    console.print(table)
    console.print(Panel.fit(
        f"[bold white]Overall Qualification:[/bold white] [{status_color}]{run_res.overall_qualification}[/{status_color}]\n"
        f"[bold white]Aggregate Score:[/bold white] [bold green]{run_res.overall_score}%[/bold green]\n"
        f"[bold white]Governance Sign-Off:[/bold white] [bold cyan]{'APPROVED' if run_res.governance_signoff else 'PENDING'}[/bold cyan]\n"
        f"[bold yellow]Recommendations:[/bold yellow]\n" + "\n".join(f"  * {r}" for r in run_res.recommended_actions),
        title="[Elite-Agent Qualification Certificate]",
        border_style=status_color,
    ))

if __name__ == "__main__":
    app()


