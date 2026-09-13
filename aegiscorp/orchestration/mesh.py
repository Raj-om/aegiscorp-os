import time
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from aegiscorp.org.hierarchy import ALL_ROLES
from aegiscorp.org.models import Role
from aegiscorp.company.db import DatabaseManager

class ChannelType(str, Enum):
    DOWNSTREAM_DELEGATION = "downstream_delegation"
    UPSTREAM_REPORTING = "upstream_reporting"
    LATERAL_PEER_SYNC = "lateral_peer_sync"
    WHISTLEBLOWER_EMERGENCY = "whistleblower_emergency"
    UNAUTHORIZED_BYPASS = "unauthorized_bypass"

class ACLCheckResult(BaseModel):
    allowed: bool
    channel_type: ChannelType
    sender_role_id: str
    recipient_role_id: str
    reason: str
    audit_flag: bool = False

class DelegationCandidate(BaseModel):
    role_id: str
    role_title: str
    department: str
    level: int
    medal_tier: str  # GOLD, SILVER, BRONZE, CERTIFIED
    composite_score: float
    domain_score: float
    is_recommended: bool
    qualification_notes: str

class CommunicationACL:
    """Agency Swarm-style Organizational Access Control List (ACL).
    Enforces corporate reporting hierarchy, preventing unauthorized rank bypasses while guaranteeing whistleblower escalations."""

    EMERGENCY_ROLES = {"board", "ceo", "cfo", "cto"}

    @classmethod
    def evaluate_message_route(
        cls,
        sender_role_id: str,
        recipient_role_id: str,
        is_emergency_flag: bool = False,
        message_topic: str = "",
    ) -> ACLCheckResult:
        sender = ALL_ROLES.get(sender_role_id)
        recipient = ALL_ROLES.get(recipient_role_id)

        if not sender or not recipient:
            return ACLCheckResult(
                allowed=False,
                channel_type=ChannelType.UNAUTHORIZED_BYPASS,
                sender_role_id=sender_role_id,
                recipient_role_id=recipient_role_id,
                reason=f"Unrecognized corporate role: sender='{sender_role_id}', recipient='{recipient_role_id}'.",
                audit_flag=True,
            )

        # 1. Whistleblower / Critical Risk Emergency Route
        if is_emergency_flag and recipient_role_id in cls.EMERGENCY_ROLES:
            return ACLCheckResult(
                allowed=True,
                channel_type=ChannelType.WHISTLEBLOWER_EMERGENCY,
                sender_role_id=sender_role_id,
                recipient_role_id=recipient_role_id,
                reason=f"Whistleblower/Fiduciary escalation granted to {recipient.title} under SOX/DGCL § 141.",
                audit_flag=True,
            )

        # 2. Upstream Direct Reporting
        if sender.reports_to == recipient_role_id:
            return ACLCheckResult(
                allowed=True,
                channel_type=ChannelType.UPSTREAM_REPORTING,
                sender_role_id=sender_role_id,
                recipient_role_id=recipient_role_id,
                reason=f"Legitimate upstream status report from {sender.title} to direct superior {recipient.title}.",
                audit_flag=False,
            )

        # 3. Downstream Delegation (Superior to subordinate in reporting line or department)
        if sender.level < recipient.level:
            # Check if direct line or executive authority
            if recipient.reports_to == sender_role_id or sender.level <= 1:
                return ACLCheckResult(
                    allowed=True,
                    channel_type=ChannelType.DOWNSTREAM_DELEGATION,
                    sender_role_id=sender_role_id,
                    recipient_role_id=recipient_role_id,
                    reason=f"Authorized executive/managerial delegation from Level {sender.level} to Level {recipient.level}.",
                    audit_flag=False,
                )
            if sender.department == recipient.department:
                return ACLCheckResult(
                    allowed=True,
                    channel_type=ChannelType.DOWNSTREAM_DELEGATION,
                    sender_role_id=sender_role_id,
                    recipient_role_id=recipient_role_id,
                    reason=f"Departmental delegation within {sender.department}.",
                    audit_flag=False,
                )

        # 4. Lateral Peer Synchronization
        if sender.level == recipient.level:
            return ACLCheckResult(
                allowed=True,
                channel_type=ChannelType.LATERAL_PEER_SYNC,
                sender_role_id=sender_role_id,
                recipient_role_id=recipient_role_id,
                reason=f"Peer-level cross-functional alignment between {sender.title} and {recipient.title} at Level {sender.level}.",
                audit_flag=False,
            )

        # 5. Unauthorized Rank Bypass
        # Example: Junior engineer (level 5) attempting to give orders or message CEO/Board without emergency flag
        return ACLCheckResult(
            allowed=False,
            channel_type=ChannelType.UNAUTHORIZED_BYPASS,
            sender_role_id=sender_role_id,
            recipient_role_id=recipient_role_id,
            reason=(
                f"Protocol Violation: {sender.title} (Level {sender.level}) cannot bypass chain of command to message "
                f"{recipient.title} (Level {recipient.level}) directly without emergency whistleblower authorization."
            ),
            audit_flag=True,
        )

class DynamicTaskDelegator:
    """CrewAI-style Dynamic Skill-Based Task Delegation.
    Selects the optimal corporate agent based on Section 31.5 calibrated 9-vector scores and medal tiers."""

    TIER_RANK = {"GOLD": 4, "SILVER": 3, "BRONZE": 2, "CERTIFIED": 1, "REMEDIATION": 0}

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    def get_department_candidates(self, department: str) -> List[Role]:
        return [r for r in ALL_ROLES.values() if r.department.lower() == department.lower()]

    def find_best_agent(
        self,
        task_title: str,
        department: str,
        required_min_tier: str = "BRONZE",
        required_authority: Optional[str] = None,
    ) -> DelegationCandidate:
        candidates = self.get_department_candidates(department)
        if not candidates:
            # Fallback to engineering or executive
            candidates = self.get_department_candidates("Engineering") or list(ALL_ROLES.values())

        scored_candidates: List[DelegationCandidate] = []
        min_tier_val = self.TIER_RANK.get(required_min_tier.upper(), 1)

        for role in candidates:
            # Check authority if specified
            if required_authority and required_authority not in role.authority:
                continue

            # Query agent profile from DB
            agent_data = self.db.get_agent(role.role_id)
            comp_score = 88.0
            domain_score = 90.0
            medal_tier = "SILVER"

            if agent_data and agent_data.get("intelligence_profile"):
                prof = agent_data["intelligence_profile"]
                comp_score = prof.get("composite_score", 88.0)
                domain_score = prof.get("domain_mastery_score", 90.0)
                medal_tier = prof.get("medal_tier", "SILVER")

            tier_val = self.TIER_RANK.get(medal_tier.upper(), 2)
            is_qualified = tier_val >= min_tier_val

            notes = (
                f"Calibrated Section 31.5 Score: {comp_score:.1f}/100 ({medal_tier} Medalist). "
                f"Meets minimum threshold '{required_min_tier}'." if is_qualified else
                f"Score {comp_score:.1f}/100 ({medal_tier}) below required '{required_min_tier}'."
            )

            scored_candidates.append(
                DelegationCandidate(
                    role_id=role.role_id,
                    role_title=role.title,
                    department=role.department,
                    level=role.level,
                    medal_tier=medal_tier,
                    composite_score=comp_score,
                    domain_score=domain_score,
                    is_recommended=is_qualified,
                    qualification_notes=notes,
                )
            )

        # Sort by: qualified first, then composite_score descending, then domain_score descending
        scored_candidates.sort(key=lambda c: (c.is_recommended, c.composite_score, c.domain_score), reverse=True)

        if not scored_candidates:
            # Fallback to department head
            dept_head = candidates[0]
            return DelegationCandidate(
                role_id=dept_head.role_id,
                role_title=dept_head.title,
                department=dept_head.department,
                level=dept_head.level,
                medal_tier="SILVER",
                composite_score=85.0,
                domain_score=88.0,
                is_recommended=True,
                qualification_notes="Fallback assigned to department head.",
            )

        best = scored_candidates[0]
        return best
