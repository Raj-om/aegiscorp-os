# AegisCorp OS 🛡️

**Governed Multi-Agent Corporate Digital Twin & Enterprise Operating System**

AegisCorp OS is a corporate digital twin and governed multi-agent operating system. It models an entire enterprise as an authoritative hierarchy of **39 specialized AI agents** with explicit reporting lines, machine-enforceable decision rights, memory systems, objective decomposition, and immutable auditability.

The system translates high-level natural language objectives into coordinated plans, decisions, tasks, and measurable business outcomes under strict corporate governance.

---

## 🏛️ Core Architecture Principles

1. **Governance Before Autonomy**: An agent may advise or execute only within its assigned scope.
2. **Deterministic High-Impact Policies**: Threshold gates ($1M, $10M, $100M, M&A) are evaluated deterministically in code, never left to LLM discretion.
3. **LLMs Propose; Validated Services Decide**: Agent models produce untrusted structured proposals. The authority graph, policy engine, and approval service determine whether an action is authorized.
4. **Immutable Decision Traceability**: Every consequential decision, approval token, tool invocation, and state variance is written to the persistent event ledger.
5. **Separation of Simulation from Reality**: Digital twin projections and paper-trading simulations are explicitly segregated from real-world external execution.

---

## 🔄 High-Level Reference Flow

```text
USER OBJECTIVE 
    → STRATEGY ENGINE 
    → AUTHORITY GRAPH 
    → EXECUTIVE DELIBERATION 
    → RISK ENGINE 
    → APPROVAL GATES 
    → DEPARTMENT PLANS 
    → EXECUTION TASK GRAPH 
    → KPI ENGINE 
    → COMPANY STATE 
    → AUDIT LEDGER 
    → BOARD / USER REPORT
```

---

## 👥 The 39-Role Corporate Hierarchy

AegisCorp OS models all 39 roles specified in the master domain architecture across the Board, Executive C-suite, and 7 departmental ladders:

```text
                                [ BOARD OF DIRECTORS ]
                                          │
                                       [ CEO ]
       ┌──────────┬──────────┬────────────┼───────────┬──────────┬──────────┬──────────┐
    [ CFO ]    [ COO ]    [ CTO ]      [ CMO ]     [ CRO ]    [ CHRO ]   [ CPO ]
       │          │          │            │           │          │          │
   Finance    Operations Engineering   Marketing    Sales      People    Product
   Ladder      Ladder     Ladder        Ladder     Ladder      Ladder    Ladder
```

### Department Ladders:
- **Executive**: Board of Directors, Chief Executive Officer (CEO).
- **Finance**: CFO, VP Finance, Finance Director, Finance Manager, Senior Analyst, Financial Analyst.
- **Operations**: COO, VP Operations, Operations Director, Operations Manager, Operations Supervisor, Operations Associate.
- **Engineering**: CTO, VP Engineering, Director Engineering, Senior Engineering Manager, Engineering Manager, Tech Lead / Staff Engineer, Senior Software Engineer, Software Engineer, Junior Engineer.
- **Marketing**: CMO, VP Marketing, Director Marketing, Marketing Manager, Marketing Specialist, Marketing Coordinator.
- **Sales**: CRO, Regional Sales Director, Sales Manager, Sales Team Lead, Account Executive, Sales Development Representative (SDR).
- **People**: CHRO, VP People, HR Director, HR Manager, HR Business Partner, HR Generalist / Coordinator.
- **Product**: CPO, VP Product, Director Product, Group Product Manager, Senior Product Manager, Product Manager, Associate Product Manager.

Each role has machine-readable definitions for:
- `role_id` & `title`
- `level` & `reports_to`
- `authority` (allowlisted capabilities)
- `approval_limits` (max capital and contractual commitment thresholds)
- `responsibilities`, `objectives`, and `kpis`
- `escalation_targets`
- `elite_domain_mastery` (PhD-level and Gold-Medalist benchmarks)

---

## ⚖️ Governance and Approval Thresholds

| Trigger | Default Gate | Policy ID |
| :--- | :--- | :--- |
| **Normal departmental work (< $1M)** | Department Owner | `POL_DELEGATED` |
| **Capital commitment &ge; $1M** | CFO Review | `POL_CAPITAL_TIER1` |
| **Capital commitment &ge; $10M** | CFO + CEO Review | `POL_CAPITAL_TIER2` |
| **Capital commitment &ge; $100M** | CFO + CEO + Board Review | `POL_CAPITAL_TIER3` |
| **Critical Risk (Score &ge; 80 / 100)** | Executive Council + Board | `POL_CRITICAL_RISK` |
| **CEO Appointment / Removal** | Board of Directors | `POL_CEO_SUCCESSION` |
| **Material M&A / Reorganization** | Board of Directors | `POL_STRUCTURAL_MA` |

Approval tokens are cryptographically generated and bound to exact decision content hashes:
$$\text{Token} = \text{SHA256}(\text{ApproverRole} \parallel \text{DecisionID} \parallel \text{VersionHash} \parallel \text{Timestamp})$$

---

## 🔬 PhD-Level & Gold-Medalist Intelligence Framework

All agents operate under the mandatory Section 31 elite intelligence standard:
- First-principles problem decomposition.
- Evidence-backed models distinguishing facts, estimates, hypotheses, forecasts, and decisions.
- Ten-point output format: Situation assessment, facts vs assumptions, options, recommendation, expected impact, risks & mitigations, dependencies, required approvals, next actions, escalation reasons.
- Adversarial review, failure-mode stress testing, and continuous learning.

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- (Optional) Docker & Docker Compose

### 1. Clone & Install
```bash
git clone https://github.com/Raj-om/aegiscorp-os.git
cd aegiscorp-os

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Launch the Web Control Plane
```bash
aegiscorp serve --port 8000
```
Open **http://127.0.0.1:8000** to interact with the real-time Enterprise Control Plane:
- 🏢 **Executive Command Center**: Digital twin telemetry, ARR, runway, and strategic programs.
- 🌳 **Live Org Hierarchy**: Visual tree and authority graph of all 39 roles.
- 🏛️ **C-Suite Rooms**: Executive functional rooms (CTO, CFO, CPO, etc.).
- 📥 **Decision Inbox**: Real-time governance approvals and cryptographic verification tokens.
- 🗼 **KPI Control Tower**: Leading and lagging metrics across 8 functional domains.
- 🔍 **Research & Discovery**: Multi-source web evaluation, candidate comparison, and license compliance.
- 📈 **Public Equities Simulator**: Segregated paper-trading portfolio with risk-adjusted Sharpe optimization.
- 🎲 **Scenario Simulator**: 500-iteration Monte Carlo forecasting for multi-trillion valuation targets.
- 📜 **Audit Explorer**: Complete immutable event stream.

---

## 💻 CLI Commands

```bash
# View corporate digital twin vital signs
aegiscorp status

# Inspect full 39-role authority graph
aegiscorp org

# Decompose a strategic objective into 7 departmental programs & run Monte Carlo
aegiscorp run-scenario "Build a $1B cybersecurity company" --budget 30000000

# View persistent audit ledger history
aegiscorp audit --limit 20
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```
AegisCorp OS will be accessible at `http://localhost:8000`.

---

## 🧪 Verification & Automated Tests

AegisCorp OS includes an end-to-end automated test suite covering:
- Role hierarchy DAG integrity & reporting chain traversal
- Policy thresholds ($1M / $10M / $100M gates) & cryptographic token verification
- Agent runtime turn lifecycle & least-privilege tool execution
- Objective decomposition across 7 departments
- Monte Carlo forecasting & public equities simulator
- REST API endpoints

Run tests with:
```bash
pytest -v tests/
```

---

## 🤖 Supported LLM Providers & Free Tier Ecosystem

AegisCorp OS provides a provider-neutral adapter layer (`aegiscorp/agents/llm.py`). Out-of-the-box, it runs fully offline with a high-fidelity deterministic simulation engine requiring **zero API keys**.

When you are ready to connect live frontier models, you can use any of the major free/open tier providers with zero credit card required:
- **Groq**: Ultra-low latency Llama 3.3 and DeepSeek R1 (`GROQ_API_KEY`)
- **OpenRouter**: Free community models (`OPENROUTER_API_KEY`)
- **GitHub Models**: Free GPT-4o and Claude 3.5 Sonnet access (`GITHUB_TOKEN`)
- **Cerebras**: High-speed Llama 3.1 70B (`CEREBRAS_API_KEY`)
- **Google Gemini**: Free API tier via Google AI Studio (`GEMINI_API_KEY`)
- **Ollama**: Local, private offline models (`llama3.2`, `qwen2.5`)

For complete setup guides and curated directories of 480+ free LLM APIs, see [`docs/FREE_LLM_PROVIDERS.md`](docs/FREE_LLM_PROVIDERS.md).

For runnable multi-agent patterns, MCP tooling, and RAG architectures, check out [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps).

---

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE).  
Copyright &copy; 2026 AegisCorp OS Contributors.
