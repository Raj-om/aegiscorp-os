import pytest
from aegiscorp.strategy.engine import StrategyEngine
from aegiscorp.execution.task_graph import ExecutionTaskGraph, ExecutionTask, TaskStatus
from aegiscorp.execution.tools import ToolGateway
from aegiscorp.execution.loop import ResearchExecutionLoop

def test_objective_decomposition_scenario():
    """Verify Section 23 scenario: 'Build a $1B cybersecurity company' decomposes into 7 departments."""
    engine = StrategyEngine()
    obj = engine.decompose_objective("Build a $1B cybersecurity company", capital_budget=30_000_000.0)

    assert len(obj.programs) == 1
    prog = obj.programs[0]
    assert len(prog.workstreams) == 7

    depts = [ws.department for ws in prog.workstreams]
    assert "Engineering" in depts
    assert "Product" in depts
    assert "Sales" in depts
    assert "Marketing" in depts
    assert "Finance" in depts
    assert "Operations" in depts
    assert "People" in depts

def test_task_graph_dependency_resolution():
    """Verify DAG task execution and dependency completion progression."""
    graph = ExecutionTaskGraph()

    t1 = ExecutionTask(id="task_arch", owner_role_id="tech_lead", title="Design Policy Architecture", description="Spec")
    t2 = ExecutionTask(id="task_impl", owner_role_id="sr_swe", title="Implement Engine", description="Code", dependencies=["task_arch"])
    t3 = ExecutionTask(id="task_deploy", owner_role_id="swe", title="Deploy Core", description="Release", dependencies=["task_impl"])

    graph.add_task(t1)
    graph.add_task(t2)
    graph.add_task(t3)

    # Initial ready task should only be t1
    ready = graph.get_ready_tasks()
    ready_ids = [t.id for t in ready]
    assert "task_arch" in ready_ids
    assert "task_impl" not in ready_ids

    # Complete t1 -> t2 should become ready
    graph.complete_task("task_arch", {"status": "spec_ready"})
    ready = graph.get_ready_tasks()
    ready_ids = [t.id for t in ready]
    assert "task_impl" in ready_ids

    # Complete t2 -> t3 should become ready
    graph.complete_task("task_impl", {"status": "code_ready"})
    ready = graph.get_ready_tasks()
    ready_ids = [t.id for t in ready]
    assert "task_deploy" in ready_ids

def test_tool_gateway_least_privilege():
    """Verify ToolGateway blocks unauthorized tools for subordinate roles."""
    gateway = ToolGateway()

    # Junior engineer cannot execute paper trade or broadcast directives
    res = gateway.execute_tool("junior_eng", "run_paper_trade", {"symbol": "NVDA", "amount": 100000.0})
    assert res.status == "REJECTED_UNAUTHORIZED"

    # Junior engineer can run linters and unit tests
    res_ok = gateway.execute_tool("junior_eng", "run_unit_tests", {})
    assert res_ok.status == "SUCCESS"

    # CFO can execute paper trade
    res_cfo = gateway.execute_tool("cfo", "run_paper_trade", {"symbol": "SPY", "amount": 50000.0})
    assert res_cfo.status == "SUCCESS"

def test_research_discovery_loop():
    """Verify Section 28.3: Discovery loop selects compliant license and records justification."""
    loop = ResearchExecutionLoop()
    record = loop.discover_and_compare("distributed vector cache")

    assert record.selected_candidate is not None
    assert "Apache-2.0" in record.selection_justification or "OpenSource" in record.selected_candidate
    assert len(record.candidates) >= 3
    # GPL candidate was not selected because of compliance constraint
    assert "Legacy-GPL-Toolkit" != record.selected_candidate
