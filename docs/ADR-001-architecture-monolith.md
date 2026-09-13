# AegisCorp OS Architecture Decision Records

## ADR-001: Modular Monolith Architecture for First Version

### Status
Accepted

### Context
AegisCorp OS requires low latency, fast iteration, unified auditability, local-first PC execution, and reproducible developer experience across Board, C-suite, and 7 departmental ladders.

### Decision
We implement AegisCorp OS as a modular monolith in Python with FastAPI, SQLite/WAL mode persistence, typed Pydantic models, and single-binary/single-command launch capability. Future distributed microservices will be split along the existing module boundaries (`org`, `governance`, `execution`, `simulation`, `finance`) when throughput or organizational scaling justifies it.

### Consequences
- Single command startup (`aegiscorp serve` or `python -m aegiscorp.cli.main serve`).
- Zero distributed system overhead for local development and simulation.
- Strict module encapsulation allows clean decoupling if services are later containerized independently.
