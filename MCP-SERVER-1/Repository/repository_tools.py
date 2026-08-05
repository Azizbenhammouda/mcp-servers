from typing import Optional
from pydantic import BaseModel, Field
from github_client import GithubClient


class License(BaseModel):
    name: Optional[str] = None


class RepositoryOutput(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    default_branch: Optional[str] = None
    language: Optional[str] = None
    stargazers_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    pushed_at: Optional[str] = None
    archived: bool = False
    private: bool = False
    html_url: Optional[str] = None
    license: Optional[License] = None


class RepositoryHandler:
    def __init__(self, client: GithubClient):
        self.client = client

    async def get_repository(self, owner: str, name: str) -> str:
        """Fetches repository details from GitHub and formats selected fields as JSON."""
        path = f"/repos/{owner}/{name}"
        data = await self.client.get(path)
        output = RepositoryOutput.model_validate(data)
        return output.model_dump_json(exclude_none=True)