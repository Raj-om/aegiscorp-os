"""AegisCorp OS — GitLab Enterprise Integration Connector.

Provides bidirectional synchronization, CI/CD pipeline triggering, and issue/MR
management with GitLab for Engineering, DevOps, and Governance roles.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from aegiscorp.agents.llm import _load_dotenv_if_present

_load_dotenv_if_present()


class GitLabIssue(BaseModel):
    id: int
    iid: int
    title: str
    description: Optional[str] = None
    state: str
    web_url: str
    author: str
    labels: List[str] = Field(default_factory=list)


class GitLabPipelineSummary(BaseModel):
    id: int
    status: str
    ref: str
    web_url: str
    created_at: str


class GitLabConnector:
    """Enterprise client for GitLab REST API v4."""

    def __init__(
        self,
        token: Optional[str] = None,
        project_id: Optional[str] = None,
        base_url: str = "https://gitlab.com/api/v4",
    ):
        self.token = token if token is not None else os.getenv("GITLAB_TOKEN")
        self.project_id = project_id if project_id is not None else os.getenv("GITLAB_PROJECT_ID", "86415735")
        self.base_url = base_url.rstrip("/")

    @property
    def is_configured(self) -> bool:
        return bool(self.token)

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["PRIVATE-TOKEN"] = self.token
        return headers

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Retrieves the authenticated user profile."""
        if not self.is_configured:
            return None
        url = f"{self.base_url}/user"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

    def get_project_metadata(self) -> Optional[Dict[str, Any]]:
        """Retrieves metadata of the configured GitLab project."""
        if not self.is_configured or not self.project_id:
            return None
        url = f"{self.base_url}/projects/{self.project_id}"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

    def list_issues(self, state: str = "opened") -> List[GitLabIssue]:
        """Lists issues in the GitLab project."""
        if not self.is_configured or not self.project_id:
            return []
        url = f"{self.base_url}/projects/{self.project_id}/issues?state={state}"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [
                    GitLabIssue(
                        id=i["id"],
                        iid=i["iid"],
                        title=i["title"],
                        description=i.get("description"),
                        state=i["state"],
                        web_url=i["web_url"],
                        author=i.get("author", {}).get("username", "unknown"),
                        labels=i.get("labels", []),
                    )
                    for i in data
                ]
        except Exception:
            return []

    def create_issue(
        self,
        title: str,
        description: str,
        labels: Optional[List[str]] = None,
    ) -> Optional[GitLabIssue]:
        """Creates a new issue in the GitLab project."""
        if not self.is_configured or not self.project_id:
            return None
        url = f"{self.base_url}/projects/{self.project_id}/issues"
        payload = {
            "title": title,
            "description": description,
            "labels": ",".join(labels or ["aegiscorp-os", "automated"]),
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                i = json.loads(resp.read().decode("utf-8"))
                return GitLabIssue(
                    id=i["id"],
                    iid=i["iid"],
                    title=i["title"],
                    description=i.get("description"),
                    state=i["state"],
                    web_url=i["web_url"],
                    author=i.get("author", {}).get("username", "unknown"),
                    labels=i.get("labels", []),
                )
        except Exception:
            return None

    def list_pipelines(self, limit: int = 10) -> List[GitLabPipelineSummary]:
        """Lists recent CI/CD pipelines in the project."""
        if not self.is_configured or not self.project_id:
            return []
        url = f"{self.base_url}/projects/{self.project_id}/pipelines?per_page={limit}"
        req = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [
                    GitLabPipelineSummary(
                        id=p["id"],
                        status=p["status"],
                        ref=p["ref"],
                        web_url=p["web_url"],
                        created_at=p["created_at"],
                    )
                    for p in data
                ]
        except Exception:
            return []

    def trigger_pipeline(self, ref: str = "main") -> Optional[Dict[str, Any]]:
        """Triggers a new CI/CD pipeline on the specified ref."""
        if not self.is_configured or not self.project_id:
            return None
        url = f"{self.base_url}/projects/{self.project_id}/pipeline?ref={ref}"
        req = urllib.request.Request(url, headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None
