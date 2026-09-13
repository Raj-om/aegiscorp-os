"""AegisCorp OS — Unit & Integration Tests for Role Training Encyclopedia Version 2.0.

Validates:
- 48 Role Learning Maps: Core capability profiles, training links, book references.
- 11 Master Learning Tracks: Content, links, and rationale.
- Shared Authoritative Reference Works & Encyclopedias.
- 7-Stage Elite-Agent Training Protocol & Adversarial Red-Team Evaluator.
- FastAPI REST Endpoints for learning maps and protocol evaluation.
- High-value reference library and evidence recording policy.
"""

import pytest
from fastapi.testclient import TestClient

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.training.learning_map import (
    ROLE_LEARNING_MAPS,
    MASTER_LEARNING_STACK,
    HIGH_VALUE_REFERENCE_LIBRARY,
    get_role_learning_map,
    list_role_learning_maps,
    get_master_learning_stack,
    get_high_value_reference_library,
    search_learning_resources,
)
from aegiscorp.training.protocol import (
    EliteTrainingProtocolRunner,
    AdversarialTestVector,
    StageEvaluationResult,
    ProtocolRunSummary,
)
from aegiscorp.training.encyclopedia import ENCYCLOPEDIA, search_encyclopedia
from aegiscorp.api.server import create_app


@pytest.fixture
def api_client():
    app = create_app()
    return TestClient(app)


class TestRoleLearningMapV2:
    def test_all_48_roles_have_learning_maps(self):
        """Verify that every role in ALL_ROLES has a corresponding Version 2.0 learning map."""
        assert len(ROLE_LEARNING_MAPS) == 48
        for role_id in ALL_ROLES:
            lm = get_role_learning_map(role_id)
            assert lm is not None, f"Role '{role_id}' missing in ROLE_LEARNING_MAPS"
            assert lm.role_id == role_id
            assert lm.role_title
            assert lm.department
            assert lm.level
            assert lm.core_capability_profile
            assert lm.role_focus_summary
            assert len(lm.training_resources) >= 2, f"Role '{role_id}' has fewer than 2 training resources"
            assert len(lm.book_references) >= 2, f"Role '{role_id}' has fewer than 2 book references"

    def test_master_learning_stack_contains_11_tracks(self):
        """Verify the 11 blueprint master learning tracks."""
        tracks = get_master_learning_stack()
        assert len(tracks) == 11
        track_names = {t.name for t in tracks}
        expected = {
            "AI / ML", "Software / CS", "Cybersecurity / Privacy",
            "Cloud / Architecture", "Product", "Business / Strategy",
            "Finance / Economics", "Operations", "People / HR",
            "Sales / Negotiation", "Marketing"
        }
        assert track_names == expected
        for t in tracks:
            assert t.starting_resources
            assert t.link.startswith("http")
            assert t.why_it_matters

    def test_high_value_reference_library(self):
        """Verify the high-value reference library index."""
        lib = get_high_value_reference_library()
        assert len(lib) >= 15
        for item in lib:
            assert "name" in item
            assert "url" in item
            assert item["url"].startswith("http")
            assert "focus" in item

    def test_search_learning_resources(self):
        """Verify cross-role search across training resources and book citations."""
        results = search_learning_resources("NIST")
        assert len(results) > 0
        assert any("NIST" in r["title"] for r in results)

        book_results = search_learning_resources("Software Engineering")
        assert len(book_results) > 0

    def test_encyclopedia_hydration_with_v2_data(self):
        """Verify that ENCYCLOPEDIA entries are automatically hydrated with Version 2.0 data."""
        cto = ENCYCLOPEDIA["cto"]
        assert cto.core_capability_profile is not None
        assert len(cto.training_resources) >= 4
        assert len(cto.book_references) >= 4

        cfo = ENCYCLOPEDIA["cfo"]
        assert cfo.core_capability_profile is not None
        assert len(cfo.training_resources) >= 3
        assert len(cfo.book_references) >= 4


class TestEliteTrainingProtocol:
    def test_protocol_adversarial_vectors(self):
        """Verify the 7 standard adversarial red-team test vectors."""
        runner = EliteTrainingProtocolRunner()
        cto = ALL_ROLES["cto"]
        vectors = runner.get_adversarial_vectors(cto)

        assert len(vectors) == 7
        categories = {v.test_category for v in vectors}
        expected_categories = {
            "authority", "hallucination", "stale_knowledge",
            "arithmetic", "bylaw_conflict", "injection", "version_drift"
        }
        assert categories == expected_categories

    def test_stage_evaluations_individually(self):
        """Verify each stage evaluation runs and produces valid scores and checks."""
        runner = EliteTrainingProtocolRunner()
        role = ALL_ROLES["cto"]

        s0 = runner.evaluate_stage_0_baseline(role)
        assert s0.stage_number == 0
        assert s0.score >= 80.0

        s1 = runner.evaluate_stage_1_foundations(role)
        assert s1.stage_number == 1
        assert s1.score >= 80.0

        s2 = runner.evaluate_stage_2_specialization(role)
        assert s2.stage_number == 2
        assert s2.score >= 60.0

        s3 = runner.evaluate_stage_3_applied_labs(role)
        assert s3.stage_number == 3
        assert s3.score >= 60.0

        s4 = runner.evaluate_stage_4_adversarial(role)
        assert s4.stage_number == 4
        assert s4.score == 100.0
        assert len(s4.adversarial_findings) == 7

        s5 = runner.evaluate_stage_5_governance(role)
        assert s5.stage_number == 5
        assert s5.score == 100.0

        s6 = runner.evaluate_stage_6_continuous_learning(role)
        assert s6.stage_number == 6
        assert s6.score >= 80.0

    def test_full_protocol_run(self):
        """Verify running the full 7-stage protocol qualification."""
        runner = EliteTrainingProtocolRunner()
        summary = runner.run_full_protocol("cto")

        assert isinstance(summary, ProtocolRunSummary)
        assert summary.role_id == "cto"
        assert summary.overall_qualification == "QUALIFIED"
        assert summary.overall_score >= 85.0
        assert summary.governance_signoff is True
        assert len(summary.stage_evaluations) == 7


class TestLearningMapAPI:
    def test_api_learning_map_overview(self, api_client):
        """GET /training/learning-map returns 11 tracks and 48 roles catalog."""
        resp = api_client.get("/training/learning-map")
        assert resp.status_code == 200
        data = resp.json()
        assert data["version"] == "2.0"
        assert len(data["master_learning_stack"]) == 11
        assert len(data["roles_catalog"]) == 48

    def test_api_single_role_learning_map(self, api_client):
        """GET /training/learning-map/{role_id} returns detailed learning map."""
        resp = api_client.get("/training/learning-map/cto")
        assert resp.status_code == 200
        data = resp.json()
        assert data["role_id"] == "cto"
        assert len(data["training_resources"]) >= 4
        assert len(data["book_references"]) >= 4

    def test_api_protocol_spec(self, api_client):
        """GET /training/protocol returns 7 stages and 7 adversarial vectors."""
        resp = api_client.get("/training/protocol")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["stages"]) == 7
        assert len(data["adversarial_test_vectors"]) == 7

    def test_api_protocol_evaluate_full(self, api_client):
        """POST /training/protocol/evaluate executes full qualification."""
        resp = api_client.post("/training/protocol/evaluate", json={"role_id": "cfo"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["role_id"] == "cfo"
        assert data["overall_qualification"] in ["QUALIFIED", "PROVISIONAL"]
        assert data["overall_score"] > 80.0

    def test_api_protocol_evaluate_single_stage(self, api_client):
        """POST /training/protocol/evaluate with stage_number executes single stage."""
        resp = api_client.post("/training/protocol/evaluate", json={"role_id": "ceo", "stage_number": 4})
        assert resp.status_code == 200
        data = resp.json()
        assert data["stage_number"] == 4
        assert data["status"] == "PASSED"
        assert len(data["adversarial_findings"]) == 7
