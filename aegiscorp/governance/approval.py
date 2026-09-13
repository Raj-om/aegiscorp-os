import hashlib
import time
import uuid
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class ApprovalRecord(BaseModel):
    approver_role_id: str
    status: ApprovalStatus
    rationale: str
    timestamp: float = Field(default_factory=time.time)
    token: str

class ApprovalRequest(BaseModel):
    id: str = Field(default_factory=lambda: f"apr_{uuid.uuid4().hex[:10]}")
    decision_id: str
    decision_version_hash: str
    requester_role_id: str
    required_approvers: List[str]
    approvals: Dict[str, ApprovalRecord] = Field(default_factory=dict)
    status: ApprovalStatus = ApprovalStatus.PENDING
    summary: str
    capital_amount: float = 0.0
    created_at: float = Field(default_factory=time.time)

class ApprovalService:
    """Manages governed approval chains and cryptographically binds approval tokens to decision versions."""
    def __init__(self):
        self.requests: Dict[str, ApprovalRequest] = {}

    def create_request(
        self,
        decision_id: str,
        decision_content: str,
        requester_role_id: str,
        required_approvers: List[str],
        summary: str,
        capital_amount: float = 0.0,
    ) -> ApprovalRequest:
        version_hash = hashlib.sha256(decision_content.encode("utf-8")).hexdigest()[:16]
        req = ApprovalRequest(
            decision_id=decision_id,
            decision_version_hash=version_hash,
            requester_role_id=requester_role_id,
            required_approvers=required_approvers,
            summary=summary,
            capital_amount=capital_amount,
        )
        self.requests[req.id] = req
        return req

    def generate_token(self, approver_role_id: str, decision_id: str, version_hash: str, timestamp: float) -> str:
        data = f"{approver_role_id}:{decision_id}:{version_hash}:{timestamp}"
        return f"tok_{hashlib.sha256(data.encode('utf-8')).hexdigest()[:24]}"

    def record_approval(
        self,
        request_id: str,
        approver_role_id: str,
        approved: bool,
        rationale: str,
    ) -> Optional[ApprovalRequest]:
        req = self.requests.get(request_id)
        if not req:
            return None

        if approver_role_id not in req.required_approvers:
            raise PermissionError(f"Role {approver_role_id} is not an authorized approver for request {request_id}")

        ts = time.time()
        status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        token = self.generate_token(approver_role_id, req.decision_id, req.decision_version_hash, ts)

        record = ApprovalRecord(
            approver_role_id=approver_role_id,
            status=status,
            rationale=rationale,
            timestamp=ts,
            token=token,
        )
        req.approvals[approver_role_id] = record

        # Check overall completion
        if not approved:
            req.status = ApprovalStatus.REJECTED
        else:
            all_approved = all(
                role in req.approvals and req.approvals[role].status == ApprovalStatus.APPROVED
                for role in req.required_approvers
            )
            if all_approved:
                req.status = ApprovalStatus.APPROVED

        return req

    def is_fully_approved(self, request_id: str) -> bool:
        req = self.requests.get(request_id)
        if not req:
            return False
        return req.status == ApprovalStatus.APPROVED

    def verify_token(self, request_id: str, approver_role_id: str, token: str) -> bool:
        req = self.requests.get(request_id)
        if not req or approver_role_id not in req.approvals:
            return False
        rec = req.approvals[approver_role_id]
        expected = self.generate_token(approver_role_id, req.decision_id, req.decision_version_hash, rec.timestamp)
        return rec.token == token and rec.token == expected
