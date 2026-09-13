import pytest
from fastapi.testclient import TestClient

from aegiscorp.execution.gitlab_connector import (
    GitLabConnector,
    GitLabIssue,
    GitLabPipelineSummary,
)
from aegiscorp.api.server import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_gitlab_connector_unconfigured():
    connector = GitLabConnector(token="")
    assert not connector.is_configured
    assert connector.get_current_user() is None
    assert connector.get_project_metadata() is None
    assert connector.list_issues() == []
    assert connector.list_pipelines() == []


def test_gitlab_connector_configured():
    connector = GitLabConnector(
        token="glpat-test-token-12345",
        project_id="86415735",
    )
    assert connector.is_configured
    assert connector.project_id == "86415735"
    headers = connector._headers()
    assert headers["PRIVATE-TOKEN"] == "glpat-test-token-12345"
    assert headers["Content-Type"] == "application/json"


def test_api_gitlab_status_unconfigured(monkeypatch):
    monkeypatch.delenv("GITLAB_TOKEN", raising=False)
    app = create_app()
    c = TestClient(app)
    res = c.get("/gitlab/status")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data


def test_api_gitlab_endpoints_exist(client):
    res_issues = client.get("/gitlab/issues")
    assert res_issues.status_code == 200
    assert isinstance(res_issues.json(), list)

    res_pipelines = client.get("/gitlab/pipelines")
    assert res_pipelines.status_code == 200
    assert isinstance(res_pipelines.json(), list)
