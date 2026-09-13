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
