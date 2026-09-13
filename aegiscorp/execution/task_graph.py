import time
import uuid
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

class ExecutionTask(BaseModel):
    id: str = Field(default_factory=lambda: f"tsk_{uuid.uuid4().hex[:8]}")
    plan_id: Optional[str] = None
    owner_role_id: str
    title: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    budget: float = 0.0
    deadline: Optional[str] = None
    acceptance_criteria: List[str] = Field(default_factory=list)
    escalation_path: str = "cto"
    status: TaskStatus = TaskStatus.PENDING
    result_output: Optional[Dict[str, Any]] = None
    created_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None

class ExecutionTaskGraph:
    """Manages directed acyclic graph (DAG) of executable corporate tasks with dependency tracking."""

    def __init__(self):
        self.tasks: Dict[str, ExecutionTask] = {}

    def add_task(self, task: ExecutionTask) -> ExecutionTask:
        self.tasks[task.id] = task
        self._refresh_task_status(task.id)
        return task

    def get_task(self, task_id: str) -> Optional[ExecutionTask]:
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[ExecutionTask]:
        return list(self.tasks.values())

    def get_ready_tasks(self) -> List[ExecutionTask]:
        """Return all tasks whose dependencies are satisfied and are ready to execute."""
        ready = []
        for task in self.tasks.values():
            if task.status in (TaskStatus.PENDING, TaskStatus.READY):
                if self._are_dependencies_satisfied(task):
                    task.status = TaskStatus.READY
                    ready.append(task)
        return ready

    def complete_task(self, task_id: str, result_output: Optional[Dict[str, Any]] = None) -> Optional[ExecutionTask]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = TaskStatus.COMPLETED
        task.result_output = result_output or {"result": "Task completed successfully"}
        task.completed_at = time.time()
        # Refresh any tasks that depend on this one
        for other in self.tasks.values():
            if task_id in other.dependencies:
                self._refresh_task_status(other.id)
        return task

    def fail_task(self, task_id: str, error_message: str) -> Optional[ExecutionTask]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = TaskStatus.FAILED
        task.result_output = {"error": error_message}
        # Mark dependents as blocked
        for other in self.tasks.values():
            if task_id in other.dependencies:
                other.status = TaskStatus.BLOCKED
        return task

    def _are_dependencies_satisfied(self, task: ExecutionTask) -> bool:
        for dep_id in task.dependencies:
            dep = self.tasks.get(dep_id)
            if not dep or dep.status != TaskStatus.COMPLETED:
                return False
        return True

    def _refresh_task_status(self, task_id: str):
        task = self.tasks.get(task_id)
        if not task or task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.IN_PROGRESS):
            return
        if any(self.tasks.get(d) and self.tasks[d].status == TaskStatus.FAILED for d in task.dependencies):
            task.status = TaskStatus.BLOCKED
        elif self._are_dependencies_satisfied(task):
            task.status = TaskStatus.READY
        else:
            task.status = TaskStatus.PENDING

    def export_graph_dict(self) -> Dict[str, Any]:
        nodes = []
        links = []
        for t in self.tasks.values():
            nodes.append({
                "id": t.id,
                "title": t.title,
                "owner": t.owner_role_id,
                "status": t.status.value,
                "budget": t.budget,
            })
            for dep in t.dependencies:
                links.append({"source": dep, "target": t.id})
        return {"nodes": nodes, "links": links}
