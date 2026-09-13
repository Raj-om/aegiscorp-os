"""Unit and integration tests for AegisCorp OS Training & Elite Agent Calibration Engine.

Verifies:
- All 48 corporate roles have complete, academically rigorous PhD curricula.
- Section 31.5 9-vector scorecard weights strictly sum to 1.0 (100%).
- Single-agent and enterprise-wide scenario tournament executions.
- IntelligenceProfile dynamic calibration and database persistence.
- PromptFactory dynamic PhD knowledge vector injection.
- FastAPI training endpoints (/training/run, /training/leaderboard, /training/curriculum/{id}).
"""

import pytest
from fastapi.testclient import TestClient

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.training import (
    CURRICULA,
    RoleCurriculum,
    TrainingTournamentEngine,
    SCORECARD_WEIGHTS,
    get_curriculum,
    get_all_curricula,
    get_department_curricula,
)
from aegiscorp.agents.prompts import PromptFactory
from aegiscorp.api.server import create_app


def test_all_48_curricula_exist_and_complete():
    """Verify that every role defined in the org hierarchy has a complete PhD curriculum."""
    assert len(CURRICULA) == 48, f"Expected 48 curricula, got {len(CURRICULA)}"
    assert len(ALL_ROLES) == 48, f"Expected 48 roles, got {len(ALL_ROLES)}"

    for role_id, role in ALL_ROLES.items():
        curr = get_curriculum(role_id)
        assert curr is not None, f"Missing curriculum for role: {role_id}"
        assert curr.role_id == role_id
        assert curr.role_title == role.title
        assert curr.department == role.department
        assert curr.level == role.level

        # Verify theoretical foundations
        assert len(curr.theoretical_foundations) >= 2, f"Role {role_id} lacks sufficient theoretical foundations"

        # Verify mathematical formulations
        assert len(curr.mathematical_formulations) >= 1, f"Role {role_id} lacks mathematical formulations"
        for mf in curr.mathematical_formulations:
            assert mf.name and mf.formula and mf.application

        # Verify landmark literature
        assert len(curr.landmark_papers) >= 1, f"Role {role_id} lacks landmark citations"
        for lp in curr.landmark_papers:
            assert lp.title and lp.authors and lp.year > 1900

        # Verify regulatory standards
        assert len(curr.regulatory_and_industry_standards) >= 1, f"Role {role_id} lacks regulatory standards"

        # Verify gold-medalist playbook
        assert len(curr.gold_medalist_playbook) >= 2, f"Role {role_id} lacks gold-medalist playbook"

        # Verify benchmark scenarios
        assert len(curr.benchmark_scenarios) >= 1, f"Role {role_id} lacks benchmark scenarios"
        for sc in curr.benchmark_scenarios:
            assert sc.scenario_id and sc.title and sc.ground_truth_criteria


def test_scorecard_weights_sum_to_one():
    """Verify Section 31.5 blueprint scorecard weights strictly sum to 100%."""
    assert abs(sum(SCORECARD_WEIGHTS.values()) - 1.0) < 1e-6
    expected_weights = {
        "domain_mastery": 0.20,
        "reasoning_quality": 0.15,
        "evidence_quality": 0.10,
        "decision_accuracy": 0.15,
        "execution_reliability": 0.15,
        "risk_discipline": 0.10,
        "collaboration": 0.05,
        "innovation": 0.05,
        "learning_velocity": 0.05,
    }
    for vector, expected in expected_weights.items():
        assert SCORECARD_WEIGHTS[vector] == expected, f"Weight mismatch for vector {vector}"


def test_department_curricula_filtering():
    """Verify department filtering returns correct subset of curricula."""
    eng_curr = get_department_curricula("Engineering")
    assert len(eng_curr) == 9  # cto + 8 ladder roles

    fin_curr = get_department_curricula("Finance")
    assert len(fin_curr) == 6  # cfo + 5 ladder roles

    prod_curr = get_department_curricula("Product")
    assert len(prod_curr) == 7  # cpo + 6 ladder roles


def test_single_agent_tournament_and_calibration():
    """Verify individual agent tournament scoring and intelligence profile calibration."""
    engine = TrainingTournamentEngine()
    result = engine.run_agent_tournament("cto")

    assert result.role_id == "cto"
    assert result.role_title == "Chief Technology Officer"
    assert result.scorecard.composite_score >= 80.0
    assert result.scorecard.medal_tier in ["GOLD", "SILVER", "BRONZE"]
    assert len(result.findings) >= 2
    assert len(result.recommendations) >= 1

    # Verify intelligence profile calibration
    prof = result.calibrated_profile
    assert prof.domain_expertise_score == result.scorecard.domain_mastery
    assert prof.reasoning_confidence == result.scorecard.reasoning_quality
    assert prof.execution_reliability == result.scorecard.execution_reliability
    assert prof.risk_discipline == result.scorecard.risk_discipline


def test_enterprise_tournament_leaderboard():
    """Verify enterprise-wide tournament runs across all 48 roles and creates ranked leaderboard."""
    engine = TrainingTournamentEngine()
    results = engine.run_enterprise_tournament()

    assert len(results) == 48
    leaderboard = engine.get_enterprise_leaderboard()
    assert len(leaderboard) == 48

    # Verify sorted descending by composite score
    scores = [r["composite_score"] for r in leaderboard]
    assert scores == sorted(scores, reverse=True)

    # Verify top role is executive or governance level
    assert leaderboard[0]["level"] <= 2


def test_prompt_factory_phd_grounding():
    """Verify PromptFactory dynamically injects PhD-level foundations into system prompts."""
    cfo_role = ALL_ROLES["cfo"]
    prompt = PromptFactory.build_system_prompt(cfo_role)

    assert "ADVANCED PhD KNOWLEDGE FOUNDATIONS:" in prompt
    assert "MATHEMATICAL & QUANTITATIVE FORMULATIONS:" in prompt
    assert "Weighted Average Cost of Capital" in prompt
    assert "Altman Z-Score" in prompt
    assert "LANDMARK CITATIONS & SCIENTIFIC LITERATURE:" in prompt
    assert "Black" in prompt or "Scholes" in prompt or "Myers" in prompt
    assert "GOLD-MEDALIST EXECUTION PLAYBOOK:" in prompt


def test_api_training_endpoints():
    """Verify FastAPI endpoints for training, leaderboard, and curriculum retrieval."""
    client = TestClient(create_app())

    # 1. Leaderboard
    r_lb = client.get("/training/leaderboard")
    assert r_lb.status_code == 200
    lb_data = r_lb.json()
    assert len(lb_data) == 48

    # 2. Role curriculum
    r_curr = client.get("/training/curriculum/board")
    assert r_curr.status_code == 200
    curr_data = r_curr.json()
    assert curr_data["role_id"] == "board"
    assert len(curr_data["theoretical_foundations"]) >= 2

    # 3. List all curricula summaries
    r_all = client.get("/training/curricula")
    assert r_all.status_code == 200
    assert len(r_all.json()) == 48

    # 4. Run single agent tournament
    r_run = client.post("/training/run", json={"role_id": "ceo"})
    assert r_run.status_code == 200
    run_data = r_run.json()
    assert run_data["role_id"] == "ceo"
    assert run_data["scorecard"]["composite_score"] >= 80.0

    # 5. Invalid role 404
    r_bad = client.get("/training/curriculum/nonexistent_role")
    assert r_bad.status_code == 404
