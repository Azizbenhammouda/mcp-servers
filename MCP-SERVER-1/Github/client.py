import sys
import httpx
from typing import Optional


class GithubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.token = token
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {token}" if token else "",
                "Accept": "application/vnd.github+json",
                "User-Agent": "MCP-GitHub-Server",
            },
        )

    async def get(self, path: str) -> dict:
        """Sends an async GET request to the GitHub API."""
        try:
            response = await self.client.get(path)
            if response.status_code != 200:
                raise RuntimeError(
                    f"GitHub API error: status {response.status_code}: {response.text}"
                )
            return response.json()
        except httpx.HTTPError as e:
            raise RuntimeError(f"Failed to perform request: {e}")

    async def close(self):
        """Cleanly close the underlying HTTP client session."""
        await self.client.aclose()