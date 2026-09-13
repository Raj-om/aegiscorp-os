import time
import uuid
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from aegiscorp.company.db import DatabaseManager

class MemoryType(str, Enum):
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    ORGANIZATIONAL = "organizational"
    FINANCIAL = "financial"
    EVALUATION = "evaluation"

class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:8]}")
    memory_type: MemoryType
    scope: str  # e.g., "global", "executive", "engineering", "finance"
    key: str
    content: Any
    importance: float = 1.0  # 0.0 to 1.0
    created_at: float = Field(default_factory=time.time)
    version: int = 1

class TieredMemorySystem:
    """Implements Section 11: 6-tier memory architecture (Working, Episodic, Semantic, Org, Financial, Eval)."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.memories: Dict[str, MemoryEntry] = {}
        self.working_memory_cache: Dict[str, Any] = {}

    def store_working(self, agent_id: str, key: str, value: Any):
        """Short-lived working memory for active task execution."""
        cache_key = f"{agent_id}:{key}"
        self.working_memory_cache[cache_key] = value

    def get_working(self, agent_id: str, key: str) -> Optional[Any]:
        return self.working_memory_cache.get(f"{agent_id}:{key}")

    def clear_working(self, agent_id: str):
        keys_to_del = [k for k in self.working_memory_cache if k.startswith(f"{agent_id}:")]
        for k in keys_to_del:
            del self.working_memory_cache[k]

    def record_memory(
        self,
        memory_type: MemoryType,
        scope: str,
        key: str,
        content: Any,
        importance: float = 0.8,
    ) -> MemoryEntry:
        """Stores persistent or long-lived episodic, semantic, organizational, financial, or evaluation memory."""
        entry = MemoryEntry(
            memory_type=memory_type,
            scope=scope,
            key=key,
            content=content,
            importance=importance,
        )
        self.memories[entry.id] = entry

        # Also write event into audit database
        self.db.record_event(
            event_id=f"evt_{uuid.uuid4().hex[:10]}",
            event_type=f"memory_stored_{memory_type.value}",
            aggregate_id=entry.id,
            actor=scope,
            payload={"key": key, "importance": importance, "type": memory_type.value},
        )
        return entry

    def query(self, memory_type: Optional[MemoryType] = None, scope: Optional[str] = None) -> List[MemoryEntry]:
        results = list(self.memories.values())
        if memory_type:
            results = [m for m in results if m.memory_type == memory_type]
        if scope:
            results = [m for m in results if m.scope == scope or m.scope == "global"]
        return sorted(results, key=lambda x: (x.importance, x.created_at), reverse=True)
