# ADR-002: Governance Before Autonomy & Deterministic Policy Enforcement

### Status
Accepted

### Context
Autonomous LLMs are prone to hallucinating actions, making out-of-scope commitments, or bypassing organizational boundaries when granted open execution permissions.

### Decision
AegisCorp OS adopts the strict principle: **LLMs propose; validated services decide whether an action is allowed.**
- Machine-readable authority graph is loaded before any prompt generation.
- Threshold gates ($1M CFO review, $10M CFO+CEO review, $100M Board review, structural M&A Board review) are enforced deterministically in Python code, completely independent of model prompt wording.
- Cryptographic approval tokens bind decisions to specific immutable versions.
- Consequential external actions require verified execution confirmation before being marked completed.

### Consequences
- Zero unauthorized approvals or executions can succeed even if an agent's prompt output asserts authorization.
- Full auditability across all decisions, approvals, and events.
