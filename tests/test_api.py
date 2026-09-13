import pytest
from fastapi.testclient import TestClient
from aegiscorp.api.server import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["governance_mode"] == "STRICT"

def test_company_state_endpoint():
    res = client.get("/company/state")
    assert res.status_code == 200
    data = res.json()
    assert data["company_name"] == "AegisCorp International"
    assert data["finance"]["cash_and_liquidity"] > 0

def test_org_endpoint():
    res = client.get("/org")
    assert res.status_code == 200
    data = res.json()
    assert data["total_roles"] >= 39
    assert len(data["roles"]) >= 39

def test_kpis_endpoint():
    res = client.get("/kpis")
    assert res.status_code == 200
    data = res.json()
    assert len(data["kpis"]) >= 15

def test_create_objective_endpoint():
    res = client.post("/objectives", json={"title": "Scale Global AI Infrastructure", "budget": 20000000.0})
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Scale Global AI Infrastructure"
    assert len(data["programs"]) > 0

def test_submit_and_approve_decision_endpoint():
    # Submit decision requiring approval
    res = client.post("/decisions", json={
        "objective": "Capital expenditure for GPU clusters",
        "proposer_role_id": "cto",
        "capital_amount": 5000000.0,
    })
    assert res.status_code == 200
    data = res.json()
    decision_id = data["turn_id"]
    assert data["status"] in ("APPROVAL_REQUIRED", "COMPLETED")

    # If approval was required, test approval endpoint
    if data.get("approval_request_id"):
        app_res = client.post(f"/decisions/{decision_id}/approve", json={
            "approver_role_id": "cfo",
            "approved": True,
            "rationale": "Approved in capital allocation review."
        })
        assert app_res.status_code == 200
        app_data = app_res.json()
        assert "cfo" in app_data["approvals"]

def test_awesome_apps_catalog_and_invocation():
    # 1. Catalog retrieval
    r_cat = client.get("/integrations/awesome-apps")
    assert r_cat.status_code == 200
    apps = r_cat.json()
    assert len(apps) >= 10
    app_ids = [a["app_id"] for a in apps]
    assert "ai_system_architect_r1" in app_ids
    assert "ai_vc_due_diligence_agent_team" in app_ids

    # 2. Authorized invocation
    r_auth = client.post("/integrations/awesome-apps/invoke", json={
        "app_id": "ai_system_architect_r1",
        "role_id": "cto",
        "inputs": {"architecture_spec": "Distributed consensus cluster", "sla_latency_p99_ms": 5.0}
    })
    assert r_auth.status_code == 200
    data_auth = r_auth.json()
    assert data_auth["status"] == "SUCCESS"
    assert data_auth["governance_check_passed"] is True
    assert data_auth["payload"]["review_score"] > 90.0

    # 3. Unauthorized invocation policy check
    r_unauth = client.post("/integrations/awesome-apps/invoke", json={
        "app_id": "ai_vc_due_diligence_agent_team",
        "role_id": "junior_eng",
        "inputs": {"target_company": "BigStartup"}
    })
    assert r_unauth.status_code == 200
    data_unauth = r_unauth.json()
    assert data_unauth["status"] == "POLICY_BLOCKED"
    assert data_unauth["governance_check_passed"] is False
