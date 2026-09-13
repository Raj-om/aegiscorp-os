"""AegisCorp OS Training & Elite Agent Intelligence Calibration Module.

Implements Section 31.5 of the AegisCorp OS Master Architecture:
- PhD-Level & Gold-Medalist Knowledge Base for all 48 corporate roles.
- 9-Vector Evaluation Scorecard (Domain Mastery, Reasoning Quality, Evidence Quality,
  Decision Accuracy, Execution Reliability, Risk Discipline, Collaboration,
  Innovation, Learning Velocity).
- Automated scenario tournament runner and intelligence profile calibration.
"""

from aegiscorp.training.knowledge_base import (
    CURRICULA,
    RoleCurriculum,
    get_curriculum,
    get_all_curricula,
    get_department_curricula,
)
from aegiscorp.training.engine import (
    TrainingTournamentEngine,
    EvaluationScorecard,
    TournamentResult,
    SCORECARD_WEIGHTS,
)
from aegiscorp.training.encyclopedia import (
    ENCYCLOPEDIA,
    EncyclopediaEntry,
    HistoricalCaseStudy,
    FailureMode,
    GlossaryTerm,
    DecisionHeuristic,
    get_role_encyclopedia,
    get_all_encyclopedias,
    search_encyclopedia,
)
from aegiscorp.training.cloud_trainer import (
    CloudTrainingOrchestrator,
    CloudTrainingJob,
    CloudProvider,
    CloudTrainingJobStatus,
    PROVIDER_PROFILES,
    WORKER_NODES,
)

__all__ = [
    "CURRICULA",
    "RoleCurriculum",
    "get_curriculum",
    "get_all_curricula",
    "get_department_curricula",
    "TrainingTournamentEngine",
    "EvaluationScorecard",
    "TournamentResult",
    "SCORECARD_WEIGHTS",
    "ENCYCLOPEDIA",
    "EncyclopediaEntry",
    "HistoricalCaseStudy",
    "FailureMode",
    "GlossaryTerm",
    "DecisionHeuristic",
    "get_role_encyclopedia",
    "get_all_encyclopedias",
    "search_encyclopedia",
    "CloudTrainingOrchestrator",
    "CloudTrainingJob",
    "CloudProvider",
    "CloudTrainingJobStatus",
    "PROVIDER_PROFILES",
    "WORKER_NODES",
]

