from typing import List, Dict, Optional, Set
from aegiscorp.org.models import Role
from aegiscorp.org.hierarchy import ALL_ROLES

class AuthorityGraph:
    def __init__(self, roles: Optional[Dict[str, Role]] = None):
        self.roles = roles or ALL_ROLES

    def get_role(self, role_id: str) -> Optional[Role]:
        return self.roles.get(role_id)

    def get_reporting_chain(self, role_id: str) -> List[Role]:
        """Return the upward chain of command from the role up to the Board."""
        chain = []
        curr = self.get_role(role_id)
        visited: Set[str] = set()
        while curr and curr.role_id not in visited:
            chain.append(curr)
            visited.add(curr.role_id)
            if not curr.reports_to or curr.reports_to in ("shareholders", "none"):
                break
            curr = self.get_role(curr.reports_to)
        return chain

    def get_subordinate_tree(self, role_id: str) -> List[Role]:
        """Return all direct and indirect subordinates under this role."""
        subordinates = []
        queue = [role_id]
        visited = {role_id}
        while queue:
            parent = queue.pop(0)
            children = [r for r in self.roles.values() if r.reports_to == parent and r.role_id not in visited]
            for child in children:
                visited.add(child.role_id)
                subordinates.append(child)
                queue.append(child.role_id)
        return subordinates

    def can_delegate_to(self, delegator_role_id: str, target_role_id: str) -> bool:
        """Check if target role is in the subordinate tree of delegator."""
        if delegator_role_id == target_role_id:
            return True
        subordinates = self.get_subordinate_tree(delegator_role_id)
        return any(sub.role_id == target_role_id for sub in subordinates)

    def resolve_escalation_target(self, role_id: str, issue_type: str = "general") -> Optional[Role]:
        """Find the immediate or designated superior to receive an escalation."""
        role = self.get_role(role_id)
        if not role:
            return None
        # Check specific escalation targets
        if role.escalation_targets:
            target_id = role.escalation_targets[0]
            return self.get_role(target_id)
        if role.reports_to and role.reports_to != "shareholders":
            return self.get_role(role.reports_to)
        return None

    def is_authorized_action(self, role_id: str, action_name: str, capital_amount: float = 0.0) -> bool:
        """Deterministic authority check: does the role have authority & spending limits?"""
        role = self.get_role(role_id)
        if not role:
            return False
        if capital_amount > role.approval_limits.max_capital_commitment:
            return False
        # Board and CEO have broad strategic authority
        if role.level <= 1:
            return True
        # Check specific capability list
        if (action_name in role.authority) or ("*" in role.authority):
            return True
        # Check tool execution gateway
        from aegiscorp.execution.tools import ToolGateway
        if ToolGateway().is_tool_allowed(role_id, action_name):
            return True
        if action_name in ("general_action", "task_execution", "evaluate_and_execute"):
            return True
        return False

    def export_graph_dict(self) -> Dict:
        """Export nodes and links for web UI visualization (D3/Mermaid/Tree)."""
        nodes = []
        links = []
        for r in self.roles.values():
            limit_val = r.approval_limits.max_capital_commitment
            if limit_val is not None and limit_val > 1e12:
                limit_val = 1_000_000_000_000_000.0
            nodes.append({
                "id": r.role_id,
                "title": r.title,
                "level": r.level,
                "department": r.department,
                "reports_to": r.reports_to,
                "limit": limit_val,
            })
            if r.reports_to and r.reports_to in self.roles:
                links.append({"source": r.reports_to, "target": r.role_id})
        return {"nodes": nodes, "links": links}
