import sqlite3
import json
import time
import os
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Persistent SQLite database manager for corporate digital twin, decisions, tasks, and audit ledger."""

    def __init__(self, db_path: str = "aegiscorp_state.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. roles
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                parent_role_id TEXT,
                department TEXT NOT NULL,
                level INTEGER NOT NULL,
                authority TEXT NOT NULL,
                approval_limits TEXT NOT NULL
            );
            """)

            # 2. agents
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                role_id TEXT NOT NULL,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                model_profile TEXT NOT NULL,
                intelligence_profile TEXT NOT NULL
            );
            """)

            # 3. policies
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id TEXT PRIMARY KEY,
                trigger TEXT NOT NULL,
                rule TEXT NOT NULL,
                approval_level TEXT NOT NULL,
                version TEXT NOT NULL
            );
            """)

            # 4. decisions
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                objective TEXT NOT NULL,
                proposer TEXT NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                risk REAL NOT NULL,
                amount REAL NOT NULL,
                payload TEXT,
                created_at REAL NOT NULL
            );
            """)

            # 5. approvals
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id TEXT PRIMARY KEY,
                decision_id TEXT NOT NULL,
                approver TEXT NOT NULL,
                status TEXT NOT NULL,
                rationale TEXT,
                token TEXT,
                timestamp REAL NOT NULL
            );
            """)

            # 6. plans
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id TEXT PRIMARY KEY,
                objective TEXT NOT NULL,
                owner TEXT NOT NULL,
                phases TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            # 7. tasks
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                plan_id TEXT,
                owner TEXT NOT NULL,
                title TEXT NOT NULL,
                dependency_ids TEXT NOT NULL,
                status TEXT NOT NULL,
                budget REAL DEFAULT 0.0,
                deadline TEXT,
                created_at REAL NOT NULL
            );
            """)

            # 8. kpis
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS kpis (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                target REAL NOT NULL,
                period TEXT NOT NULL,
                owner TEXT NOT NULL,
                domain TEXT NOT NULL
            );
            """)

            # 9. company_state
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_state (
                id TEXT PRIMARY KEY,
                cash REAL NOT NULL,
                revenue REAL NOT NULL,
                headcount INTEGER NOT NULL,
                risk_score REAL NOT NULL,
                state_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                updated_at REAL NOT NULL
            );
            """)

            # 10. events (Audit Ledger)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                aggregate_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp REAL NOT NULL
            );
            """)

            # 11. memories
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                scope TEXT NOT NULL,
                content_ref TEXT NOT NULL,
                importance REAL NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            # 12. tool_runs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_runs (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                tool TEXT NOT NULL,
                arguments_hash TEXT NOT NULL,
                result_ref TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp REAL NOT NULL
            );
            """)

            # 13. evaluations
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                scenario TEXT NOT NULL,
                score REAL NOT NULL,
                findings TEXT NOT NULL,
                timestamp REAL NOT NULL
            );
            """)

            # 14. cloud_training_jobs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cloud_training_jobs (
                id TEXT PRIMARY KEY,
                role_id TEXT NOT NULL,
                role_title TEXT NOT NULL,
                department TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                worker_node TEXT NOT NULL,
                region TEXT NOT NULL,
                status TEXT NOT NULL,
                tokens_processed INTEGER NOT NULL,
                throughput_tok_sec REAL NOT NULL,
                latency_ms REAL NOT NULL,
                cost_usd REAL NOT NULL,
                initial_score REAL NOT NULL,
                final_score REAL NOT NULL,
                score_delta REAL NOT NULL,
                medal_tier TEXT NOT NULL,
                epochs INTEGER NOT NULL,
                logs TEXT NOT NULL,
                started_at REAL NOT NULL,
                completed_at REAL
            );
            """)

            # 15. orchestration_traces
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orchestration_traces (
                trace_id TEXT PRIMARY KEY,
                initiative TEXT NOT NULL,
                status TEXT NOT NULL,
                total_cost_usd REAL NOT NULL,
                total_tokens INTEGER NOT NULL,
                duration_ms REAL NOT NULL,
                spans_json TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            # 16. orchestration_debates
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orchestration_debates (
                debate_id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                role_a TEXT NOT NULL,
                role_b TEXT NOT NULL,
                consensus_score REAL NOT NULL,
                is_approved INTEGER NOT NULL,
                verdict_json TEXT NOT NULL,
                rounds_json TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            # 17. orchestration_artifacts
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orchestration_artifacts (
                bundle_id TEXT PRIMARY KEY,
                initiative TEXT NOT NULL,
                prd_json TEXT,
                architecture_json TEXT,
                financial_json TEXT,
                gtm_json TEXT,
                security_json TEXT,
                runbook_json TEXT,
                is_fully_signed_off INTEGER NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            conn.commit()

    def record_event(self, event_id: str, event_type: str, aggregate_id: str, actor: str, payload: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO events (id, type, aggregate_id, actor, payload, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (event_id, event_type, aggregate_id, actor, json.dumps(payload), time.time()),
            )
            conn.commit()

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, type, aggregate_id, actor, payload, timestamp FROM events ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "type": r["type"],
                    "aggregate_id": r["aggregate_id"],
                    "actor": r["actor"],
                    "payload": json.loads(r["payload"]) if r["payload"] else {},
                    "timestamp": r["timestamp"],
                })
            return results

    def save_decision(self, decision_data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO decisions (id, objective, proposer, owner, status, risk, amount, payload, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision_data["id"],
                    decision_data["objective"],
                    decision_data["proposer"],
                    decision_data["owner"],
                    decision_data["status"],
                    decision_data.get("risk", 0.0),
                    decision_data.get("amount", 0.0),
                    json.dumps(decision_data.get("payload", {})),
                    decision_data.get("created_at", time.time()),
                ),
            )
            conn.commit()

    def get_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM decisions WHERE id = ?", (decision_id,))
            r = cursor.fetchone()
            if not r:
                return None
            return {
                "id": r["id"],
                "objective": r["objective"],
                "proposer": r["proposer"],
                "owner": r["owner"],
                "status": r["status"],
                "risk": r["risk"],
                "amount": r["amount"],
                "payload": json.loads(r["payload"]) if r["payload"] else {},
                "created_at": r["created_at"],
            }

    def list_decisions(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM decisions ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "objective": r["objective"],
                    "proposer": r["proposer"],
                    "owner": r["owner"],
                    "status": r["status"],
                    "risk": r["risk"],
                    "amount": r["amount"],
                    "payload": json.loads(r["payload"]) if r["payload"] else {},
                    "created_at": r["created_at"],
                }
                for r in rows
            ]

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM agents WHERE id = ? OR role_id = ?", (agent_id, agent_id))
            r = cursor.fetchone()
            if not r:
                return None
            return {
                "id": r["id"],
                "role_id": r["role_id"],
                "name": r["name"],
                "status": r["status"],
                "model_profile": json.loads(r["model_profile"]) if r["model_profile"] else {},
                "intelligence_profile": json.loads(r["intelligence_profile"]) if r["intelligence_profile"] else {},
            }

    def save_agent(self, agent_data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO agents (id, role_id, name, status, model_profile, intelligence_profile)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                agent_data["id"],
                agent_data["role_id"],
                agent_data.get("name", agent_data["role_id"].upper()),
                agent_data.get("status", "ACTIVE"),
                json.dumps(agent_data.get("model_profile", {})),
                json.dumps(agent_data.get("intelligence_profile", {})),
            ))
            conn.commit()

    def list_agents(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM agents")
            rows = cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "role_id": r["role_id"],
                    "name": r["name"],
                    "status": r["status"],
                    "model_profile": json.loads(r["model_profile"]) if r["model_profile"] else {},
                    "intelligence_profile": json.loads(r["intelligence_profile"]) if r["intelligence_profile"] else {},
                }
                for r in rows
            ]

    def save_cloud_training_job(self, job_data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cloud_training_jobs (
                    id, role_id, role_title, department, provider, model,
                    worker_node, region, status, tokens_processed, throughput_tok_sec,
                    latency_ms, cost_usd, initial_score, final_score, score_delta,
                    medal_tier, epochs, logs, started_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_data["id"],
                    job_data["role_id"],
                    job_data["role_title"],
                    job_data["department"],
                    job_data["provider"],
                    job_data["model"],
                    job_data["worker_node"],
                    job_data["region"],
                    job_data["status"],
                    job_data["tokens_processed"],
                    job_data["throughput_tok_sec"],
                    job_data["latency_ms"],
                    job_data["cost_usd"],
                    job_data["initial_score"],
                    job_data["final_score"],
                    job_data["score_delta"],
                    job_data["medal_tier"],
                    job_data["epochs"],
                    json.dumps(job_data.get("logs", [])),
                    job_data["started_at"],
                    job_data.get("completed_at"),
                )
            )
            conn.commit()

    def get_cloud_training_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM cloud_training_jobs WHERE id = ?", (job_id,))
            r = cursor.fetchone()
            if not r:
                return None
            return {
                "id": r["id"],
                "role_id": r["role_id"],
                "role_title": r["role_title"],
                "department": r["department"],
                "provider": r["provider"],
                "model": r["model"],
                "worker_node": r["worker_node"],
                "region": r["region"],
                "status": r["status"],
                "tokens_processed": r["tokens_processed"],
                "throughput_tok_sec": r["throughput_tok_sec"],
                "latency_ms": r["latency_ms"],
                "cost_usd": r["cost_usd"],
                "initial_score": r["initial_score"],
                "final_score": r["final_score"],
                "score_delta": r["score_delta"],
                "medal_tier": r["medal_tier"],
                "epochs": r["epochs"],
                "logs": json.loads(r["logs"]) if r["logs"] else [],
                "started_at": r["started_at"],
                "completed_at": r["completed_at"],
            }

    def list_cloud_training_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM cloud_training_jobs ORDER BY started_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "role_id": r["role_id"],
                    "role_title": r["role_title"],
                    "department": r["department"],
                    "provider": r["provider"],
                    "model": r["model"],
                    "worker_node": r["worker_node"],
                    "region": r["region"],
                    "status": r["status"],
                    "tokens_processed": r["tokens_processed"],
                    "throughput_tok_sec": r["throughput_tok_sec"],
                    "latency_ms": r["latency_ms"],
                    "cost_usd": r["cost_usd"],
                    "initial_score": r["initial_score"],
                    "final_score": r["final_score"],
                    "score_delta": r["score_delta"],
                    "medal_tier": r["medal_tier"],
                    "epochs": r["epochs"],
                    "logs": json.loads(r["logs"]) if r["logs"] else [],
                    "started_at": r["started_at"],
                    "completed_at": r["completed_at"],
                }
                for r in rows
            ]

    # --- Enterprise Orchestration Methods ---

    def save_orchestration_trace(self, trace: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO orchestration_traces (
                trace_id, initiative, status, total_cost_usd, total_tokens, duration_ms, spans_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trace["trace_id"],
                trace["initiative"],
                trace["status"],
                trace["total_cost_usd"],
                trace["total_tokens"],
                trace["duration_ms"],
                json.dumps(trace.get("spans", [])),
                trace.get("created_at", time.time()),
            ))
            conn.commit()

    def get_orchestration_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM orchestration_traces WHERE trace_id = ?", (trace_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "trace_id": row["trace_id"],
                "initiative": row["initiative"],
                "status": row["status"],
                "total_cost_usd": row["total_cost_usd"],
                "total_tokens": row["total_tokens"],
                "duration_ms": row["duration_ms"],
                "spans": json.loads(row["spans_json"]) if row["spans_json"] else [],
                "created_at": row["created_at"],
            }

    def list_orchestration_traces(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM orchestration_traces ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "trace_id": r["trace_id"],
                    "initiative": r["initiative"],
                    "status": r["status"],
                    "total_cost_usd": r["total_cost_usd"],
                    "total_tokens": r["total_tokens"],
                    "duration_ms": r["duration_ms"],
                    "spans": json.loads(r["spans_json"]) if r["spans_json"] else [],
                    "created_at": r["created_at"],
                }
                for r in rows
            ]

    def save_debate_record(self, debate: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO orchestration_debates (
                debate_id, topic, role_a, role_b, consensus_score, is_approved, verdict_json, rounds_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                debate["debate_id"],
                debate["topic"],
                debate["role_a"],
                debate["role_b"],
                debate["verdict"]["consensus_score"],
                1 if debate["verdict"]["is_approved"] else 0,
                json.dumps(debate["verdict"]),
                json.dumps(debate.get("rounds", [])),
                debate.get("created_at", time.time()),
            ))
            conn.commit()

    def get_debate_record(self, debate_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM orchestration_debates WHERE debate_id = ?", (debate_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "debate_id": row["debate_id"],
                "topic": row["topic"],
                "role_a": row["role_a"],
                "role_b": row["role_b"],
                "consensus_score": row["consensus_score"],
                "is_approved": bool(row["is_approved"]),
                "verdict": json.loads(row["verdict_json"]) if row["verdict_json"] else {},
                "rounds": json.loads(row["rounds_json"]) if row["rounds_json"] else [],
                "created_at": row["created_at"],
            }

    def list_debate_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM orchestration_debates ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "debate_id": r["debate_id"],
                    "topic": r["topic"],
                    "role_a": r["role_a"],
                    "role_b": r["role_b"],
                    "consensus_score": r["consensus_score"],
                    "is_approved": bool(r["is_approved"]),
                    "verdict": json.loads(r["verdict_json"]) if r["verdict_json"] else {},
                    "rounds": json.loads(r["rounds_json"]) if r["rounds_json"] else [],
                    "created_at": r["created_at"],
                }
                for r in rows
            ]

    def save_sop_bundle(self, bundle: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO orchestration_artifacts (
                bundle_id, initiative, prd_json, architecture_json, financial_json, gtm_json, security_json, runbook_json, is_fully_signed_off, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                bundle["bundle_id"],
                bundle["initiative"],
                json.dumps(bundle.get("prd")),
                json.dumps(bundle.get("architecture_spec")),
                json.dumps(bundle.get("financial_model")),
                json.dumps(bundle.get("gtm_plan")),
                json.dumps(bundle.get("security_assessment")),
                json.dumps(bundle.get("runbook")),
                1 if bundle.get("is_fully_signed_off") else 0,
                bundle.get("created_at", time.time()),
            ))
            conn.commit()

    def get_sop_bundle(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM orchestration_artifacts WHERE bundle_id = ?", (bundle_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "bundle_id": row["bundle_id"],
                "initiative": row["initiative"],
                "prd": json.loads(row["prd_json"]) if row["prd_json"] else None,
                "architecture_spec": json.loads(row["architecture_json"]) if row["architecture_json"] else None,
                "financial_model": json.loads(row["financial_json"]) if row["financial_json"] else None,
                "gtm_plan": json.loads(row["gtm_json"]) if row["gtm_json"] else None,
                "security_assessment": json.loads(row["security_json"]) if row["security_json"] else None,
                "runbook": json.loads(row["runbook_json"]) if row["runbook_json"] else None,
                "is_fully_signed_off": bool(row["is_fully_signed_off"]),
                "created_at": row["created_at"],
            }


