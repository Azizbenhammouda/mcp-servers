# GitHub MCP Server

An MCP (Model Context Protocol) server that enables AI assistants to interact with GitHub repositories through a secure, structured interface.

The server exposes GitHub functionality as MCP tools, resources, and prompts, allowing LLMs to inspect repositories, manage issues, review pull requests, and automate common development workflows.

---

## Features

### Repository Management

- View repository information
- Search repositories
- List branches
- List tags
- Browse repository contents
- Read files
- Search code

### Issues

- List issues
- Create issues
- Update issues
- Close/Reopen issues
- Search issues
- Add comments
- Assign users
- Manage labels

### Pull Requests

- List pull requests
- Create pull requests
- Review pull requests
- Merge pull requests
- View changed files
- Add review comments

### Commits

- List commits
- View commit details
- Compare commits
- View commit history

### Releases

- List releases
- Create releases
- Generate release notes

### Workflows

- List GitHub Actions workflows
- Trigger workflows
- View workflow runs
- Inspect workflow logs

---

## MCP Components

### Tools

| Tool | Description |
|-------|-------------|
| `list_repositories` | List accessible repositories |
| `get_repository` | Retrieve repository metadata |
| `search_repositories` | Search public and private repositories |
| `list_issues` | List repository issues |
| `create_issue` | Create a new GitHub issue |
| `update_issue` | Update an existing issue |
| `list_pull_requests` | List pull requests |
| `create_pull_request` | Create a pull request |
| `review_pull_request` | Submit a review |
| `list_commits` | View commit history |
| `search_code` | Search code across repositories |
| `read_file` | Retrieve repository file contents |
| `list_workflows` | List GitHub Actions workflows |

More tools will be added as the project evolves.

---

### Resources

The server exposes useful GitHub resources, including:

- Repository metadata
- README files
- Pull request details
- Commit history
- Repository tree
- Workflow information

---

### Prompts

Built-in prompts simplify common development tasks.

Examples:

- Review a pull request
- Generate release notes
- Summarize repository activity
- Find beginner-friendly issues
- Explain project architecture
- Analyze repository health

---

## Authentication

Authentication is performed using a GitHub Personal Access Token.

Required scopes depend on enabled features.

Typical permissions include:

- Repository access
- Pull requests
- Issues
- Actions
- Metadata

---

## Configuration

Example configuration:

```json
{
  "github_token": "<your-token>",
  "default_owner": "your-username",
  "default_repository": "your-repository"
}
```

---

## Example Use Cases

### Code Review

> Review the latest pull request and summarize the requested changes.

---

### Repository Exploration

> Explain the architecture of this repository.

---

### Issue Management

> Create a bug report for the authentication failure.

---

### Release Automation

> Generate release notes from commits since the last release.

---

### CI/CD Inspection

> Show the latest failed GitHub Actions workflow and explain why it failed.

---

## Project Structure

```
github-mcp/
├── go.mod
├── go.sum
├──main.go  
├── Repository/     
    ├── types.go          // input structs 
    ├── tools.go           
    ├── resources.go        
    └── prompts.go   
```



