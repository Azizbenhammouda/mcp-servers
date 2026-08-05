import os
import sys
from mcp.server.fastmcp import FastMCP
from github_client import GithubClient
from repository_handler import RepositoryHandler

# Initialize FastMCP Server
mcp = FastMCP("Github Server")

# Check for required GITHUB_TOKEN environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("GITHUB_TOKEN environment variable is required", file=sys.stderr)
    sys.exit(1)

# Initialize GitHub Client & Handler
github_client = GithubClient(token)
handler = RepositoryHandler(github_client)


@mcp.tool(
    name="get_repository",
    description="Get information about a GitHub repository",
)
async def get_repository(owner: str, name: str) -> str:
    """Gets information about a GitHub repository."""
    return await handler.get_repository(owner=owner, name=name)


if __name__ == "__main__":
    mcp.run(transport="stdio")