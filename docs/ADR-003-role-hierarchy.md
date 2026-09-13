# ADR-003: Structured 39-Role Organizational Hierarchy

### Status
Accepted

### Context
Section 5, 6, and 31 of the AegisCorp OS Master Document define a 39-role corporate hierarchy spanning the Board of Directors, CEO, 8 C-suite executives, and 7 functional department ladders (Engineering, Product, Sales, Marketing, Finance, Operations, People).

### Decision
All 39 roles are encoded as first-class, machine-readable records with:
- `role_id`: Stable identifier (e.g. `cto`, `vp_eng`, `tech_lead`, `sr_swe`)
- `title`: Human-readable title
- `level`: Authority depth (0=Board, 1=CEO, 2=C-suite, 3=VP, 4=Director, 5=Manager/Lead, 6=IC)
- `reports_to`: Explicit reporting parent ID
- `department`: Functional domain
- `authority`: Strict capability allowlist
- `approval_limits`: Max capital and operational commitment threshold
- `kpis`: Metrics owned or influenced
- `escalation_targets`: Specific roles for escalation
- `constraints`: Specific prohibited policies

Role prompts are dynamically generated from this structured metadata rather than one giant static prompt.
