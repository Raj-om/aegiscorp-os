import pytest
from aegiscorp.org.hierarchy import ALL_ROLES, get_role_by_id, get_subordinates, get_ladder_roles
from aegiscorp.org.graph import AuthorityGraph

def test_all_39_roles_present():
    """Verify that all roles specified in the master blueprint are present (at least 39)."""
    assert len(ALL_ROLES) >= 39
    assert "board" in ALL_ROLES
    assert "ceo" in ALL_ROLES
    assert "cfo" in ALL_ROLES
    assert "coo" in ALL_ROLES
    assert "cto" in ALL_ROLES
    assert "cmo" in ALL_ROLES
    assert "cro" in ALL_ROLES
    assert "chro" in ALL_ROLES
    assert "cpo" in ALL_ROLES

def test_department_ladders_complete():
    """Verify each department ladder exists and has appropriate hierarchical levels."""
    eng_roles = get_ladder_roles("Engineering")
    assert len(eng_roles) >= 8  # CTO, VP Eng, Dir Eng, Sr Eng Mgr, Eng Mgr, Tech Lead, Sr SWE, SWE, Jr Eng

    prod_roles = get_ladder_roles("Product")
    assert len(prod_roles) >= 6  # CPO, VP Prod, Dir Prod, GPM, Sr PM, PM, APM

    sales_roles = get_ladder_roles("Sales")
    assert len(sales_roles) >= 5  # CRO, Reg Sales Dir, Sales Mgr, Team Lead, AE, SDR

    mktg_roles = get_ladder_roles("Marketing")
    assert len(mktg_roles) >= 5

    fin_roles = get_ladder_roles("Finance")
    assert len(fin_roles) >= 5

    ops_roles = get_ladder_roles("Operations")
    assert len(ops_roles) >= 5

    people_roles = get_ladder_roles("People")
    assert len(people_roles) >= 5

def test_reporting_chain_upward():
    """Verify reporting chain from junior engineer traverses up to Board."""
    graph = AuthorityGraph()
    chain = graph.get_reporting_chain("junior_eng")
    chain_ids = [r.role_id for r in chain]

    assert "swe" in chain_ids
    assert "sr_swe" in chain_ids
    assert "tech_lead" in chain_ids
    assert "eng_mgr" in chain_ids
    assert "sr_eng_mgr" in chain_ids
    assert "director_eng" in chain_ids
    assert "vp_eng" in chain_ids
    assert "cto" in chain_ids
    assert "ceo" in chain_ids
    assert "board" in chain_ids

def test_authority_limits_enforced():
    """Verify that approval limits are strictly enforced deterministically."""
    graph = AuthorityGraph()
    # Junior engineer cannot authorize $50,000 capital commitment
    assert not graph.is_authorized_action("junior_eng", "purchase_tool", 50000.0)
    # Junior engineer has 0 limit
    assert graph.get_role("junior_eng").approval_limits.max_capital_commitment == 0.0

    # Tech lead has $20,000 limit
    assert graph.is_authorized_action("tech_lead", "system_design", 15000.0)
    assert not graph.is_authorized_action("tech_lead", "system_design", 25000.0)

    # CFO has $10M limit
    assert graph.is_authorized_action("cfo", "budgeting", 8000000.0)
    assert not graph.is_authorized_action("cfo", "budgeting", 15000000.0)

def test_escalation_target_resolution():
    """Verify that out-of-scope tasks resolve to the correct escalation superior."""
    graph = AuthorityGraph()
    target = graph.resolve_escalation_target("swe")
    assert target is not None
    assert target.role_id == "sr_swe"

    cto_target = graph.resolve_escalation_target("cto")
    assert cto_target is not None
    assert cto_target.role_id == "ceo"
