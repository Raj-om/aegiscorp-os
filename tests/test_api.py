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
