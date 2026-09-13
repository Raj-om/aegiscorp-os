import pytest
from fastapi.testclient import TestClient

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.training.encyclopedia import (
    ENCYCLOPEDIA,
    get_role_encyclopedia,
    get_all_encyclopedias,
    search_encyclopedia,
)
from aegiscorp.training.cloud_trainer import (
    CloudTrainingOrchestrator,
    CloudTrainingJobStatus,
    PROVIDER_PROFILES,
    WORKER_NODES,
)
from aegiscorp.company.db import DatabaseManager
from aegiscorp.api.server import create_app


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_cloud_training.db"
    return DatabaseManager(db_path=str(db_file))


@pytest.fixture
def cloud_orchestrator(test_db):
    return CloudTrainingOrchestrator(db=test_db)


@pytest.fixture
def client(test_db):
    app = create_app()
    return TestClient(app)


# -----------------------------------------------------------------------------
# 1. ENCYCLOPEDIA UNIT TESTS
# -----------------------------------------------------------------------------

def test_encyclopedia_covers_all_48_roles():
    """Verify that every single of the 48 corporate roles has an encyclopedic dossier."""
    assert len(ENCYCLOPEDIA) == 48
    for role_id in ALL_ROLES.keys():
        entry = get_role_encyclopedia(role_id)
        assert entry is not None, f"Missing encyclopedia for role '{role_id}'"
        assert entry.role_id == role_id
        assert len(entry.canonical_definition) > 30
        assert len(entry.core_mandate) > 15
        assert len(entry.historical_case_studies) >= 1
        assert len(entry.failure_modes) >= 1
        assert len(entry.key_glossary) >= 1
        assert len(entry.decision_heuristics) >= 1


def test_encyclopedia_case_studies_quality():
    """Verify historical precedents for key C-Suite and Board roles."""
    board_entry = get_role_encyclopedia("board")
    assert any("Enron" in cs.organization for cs in board_entry.historical_case_studies)
    assert any("Theranos" in cs.organization for cs in board_entry.historical_case_studies)

    cto_entry = get_role_encyclopedia("cto")
    assert any("Knight Capital" in cs.organization for cs in cto_entry.historical_case_studies)
    assert any("Equifax" in cs.organization for cs in cto_entry.historical_case_studies)

    coo_entry = get_role_encyclopedia("coo")
    assert any("Boeing" in cs.organization for cs in coo_entry.historical_case_studies)

    cfo_entry = get_role_encyclopedia("cfo")
    assert any("Lehman" in cs.organization for cs in cfo_entry.historical_case_studies)


def test_encyclopedia_search():
    """Verify relevance search across definitions, cases, failure modes, and glossaries."""
    # Search for Enron
    res_enron = search_encyclopedia("Enron")
    assert len(res_enron) >= 2
    matched_ids = [r["role_id"] for r in res_enron]
    assert "board" in matched_ids
    assert "chro" in matched_ids

    # Search for Boeing
    res_boeing = search_encyclopedia("Boeing")
    assert len(res_boeing) >= 1
    assert res_boeing[0]["role_id"] == "coo"

    # Search for Fiduciary
    res_fiduciary = search_encyclopedia("fiduciary")
    assert len(res_fiduciary) >= 1
    assert res_fiduciary[0]["role_id"] in ("board", "cfo", "ceo")

    # Search for Latency
    res_latency = search_encyclopedia("latency")
    assert len(res_latency) >= 1

    # Search with role_id filter
    res_scoped = search_encyclopedia("Enron", role_id="board")
    assert len(res_scoped) == 1
    assert res_scoped[0]["role_id"] == "board"


# -----------------------------------------------------------------------------
# 2. CLOUD TRAINING ORCHESTRATOR UNIT TESTS
# -----------------------------------------------------------------------------

def test_cloud_providers_and_workers(cloud_orchestrator):
    """Verify supported providers and worker nodes."""
    providers = cloud_orchestrator.get_supported_providers()
    assert len(providers) == 8
    prov_ids = [p["id"] for p in providers]
    assert "groq" in prov_ids
    assert "openrouter" in prov_ids
    assert "gemini" in prov_ids
    assert "cloud_cluster" in prov_ids

    workers = cloud_orchestrator.get_worker_nodes()
    assert len(workers) == len(WORKER_NODES)
    assert any(w["region"] == "us-east-1" for w in workers)


def test_dispatch_single_cloud_job(cloud_orchestrator, test_db):
    """Verify dispatching a cloud training job updates score, persists to DB, and logs telemetry."""
    job = cloud_orchestrator.dispatch_job(
        role_id="cfo",
        provider="groq",
        epochs=3,
    )

    assert job.id.startswith("cjob_")
    assert job.role_id == "cfo"
    assert job.provider == "groq"
    assert job.status == CloudTrainingJobStatus.COMPLETED
    assert job.tokens_processed > 0
    assert job.throughput_tok_sec > 0
    assert job.latency_ms > 0
    assert job.cost_usd >= 0.0
    assert job.final_score >= job.initial_score
    assert job.medal_tier in ("GOLD", "SILVER", "BRONZE")
    assert len(job.logs) >= 5

    # Check persistence in DB
    retrieved = cloud_orchestrator.get_job(job.id)
    assert retrieved is not None
    assert retrieved.id == job.id
    assert retrieved.role_title == job.role_title

    # Check telemetry update
    telem = cloud_orchestrator.get_cluster_telemetry()
    assert telem["total_jobs_completed"] == 1
    assert telem["total_tokens_processed"] == job.tokens_processed
    assert telem["total_cost_usd"] > 0.0


def test_dispatch_batch_cloud_jobs(cloud_orchestrator):
    """Verify dispatching batch cloud training across selected roles."""
    target_roles = ["board", "ceo", "cto"]
    jobs = cloud_orchestrator.dispatch_batch_jobs(
        provider="cloud_cluster",
        role_ids=target_roles,
    )
    assert len(jobs) == 3
    for j in jobs:
        assert j.status == CloudTrainingJobStatus.COMPLETED
        assert j.role_id in target_roles
        assert j.score_delta > 0

    telem = cloud_orchestrator.get_cluster_telemetry()
    assert telem["total_jobs_completed"] == 3


def test_dispatch_mesh_routing_cloud_jobs(cloud_orchestrator):
    """Verify multi-cloud dynamic mesh routes roles to specialized cloud providers."""
    roles = ["ceo", "cto", "cfo", "cpo", "coo", "cro"]
    jobs = cloud_orchestrator.dispatch_batch_jobs(
        provider="mesh",
        role_ids=roles,
    )
    assert len(jobs) == 6
    provider_map = {j.role_id: j.provider for j in jobs}
    assert provider_map["ceo"] == "gemini"
    assert provider_map["cto"] == "cerebras"
    assert provider_map["cfo"] == "mistral"
    assert provider_map["cpo"] == "github_models"
    assert provider_map["coo"] == "groq"
    assert provider_map["cro"] == "openrouter"


def test_invalid_role_cloud_dispatch(cloud_orchestrator):
    """Verify error on invalid role dispatch."""
    with pytest.raises(ValueError):
        cloud_orchestrator.dispatch_job(role_id="non_existent_role_xyz")


# -----------------------------------------------------------------------------
# 3. API INTEGRATION TESTS
# -----------------------------------------------------------------------------

def test_api_list_encyclopedias(client):
    res = client.get("/training/encyclopedia")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 48
    assert "role_id" in data[0]
    assert "core_mandate" in data[0]


def test_api_get_single_encyclopedia(client):
    res = client.get("/training/encyclopedia/board")
    assert res.status_code == 200
    data = res.json()
    assert data["role_id"] == "board"
    assert len(data["historical_case_studies"]) >= 2
    assert len(data["failure_modes"]) >= 2

    # 404 for non-existent role
    res_404 = client.get("/training/encyclopedia/non_existent_role")
    assert res_404.status_code == 404


def test_api_search_encyclopedia(client):
    res = client.get("/training/encyclopedia/search?q=Knight Capital")
    assert res.status_code == 200
    results = res.json()
    assert len(results) >= 1
    assert any(r["role_id"] == "cto" for r in results)


def test_api_cloud_providers_and_telemetry(client):
    res_p = client.get("/training/cloud/providers")
    assert res_p.status_code == 200
    providers = res_p.json()
    assert len(providers) == 8

    res_t = client.get("/training/cloud/telemetry")
    assert res_t.status_code == 200
    telem = res_t.json()
    assert "active_workers" in telem
    assert "total_tokens_processed" in telem


def test_api_dispatch_cloud_training(client):
    # Single role dispatch
    res = client.post(
        "/training/cloud/dispatch",
        json={"role_id": "cto", "provider": "groq", "epochs": 2},
    )
    assert res.status_code == 200
    job = res.json()
    assert job["role_id"] == "cto"
    assert job["status"] == "COMPLETED"

    # List jobs
    res_jobs = client.get("/training/cloud/jobs")
    assert res_jobs.status_code == 200
    jobs_list = res_jobs.json()
    assert len(jobs_list) >= 1
    assert jobs_list[0]["id"] == job["id"]

    # Get single job
    res_single = client.get(f"/training/cloud/jobs/{job['id']}")
    assert res_single.status_code == 200
    assert res_single.json()["id"] == job["id"]
