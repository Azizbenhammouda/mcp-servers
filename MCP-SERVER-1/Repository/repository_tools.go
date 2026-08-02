package Repository

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/Azizbenhammouda/MCP-SERVERS/MCP-SERVER-1/Github"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type License struct {
	Name string `json:"name"`
}

type RepositoryOutput struct {
	Name            string   `json:"name"`
	FullName        string   `json:"full_name"`
	Description     string   `json:"description"`
	DefaultBranch   string   `json:"default_branch"`
	Language        string   `json:"language"`
	StargazersCount int      `json:"stargazers_count"`
	ForksCount      int      `json:"forks_count"`
	OpenIssuesCount int      `json:"open_issues_count"`
	CreatedAt       string   `json:"created_at"`
	UpdatedAt       string   `json:"updated_at"`
	PushedAt        string   `json:"pushed_at"`
	Archived        bool     `json:"archived"`
	Private         bool     `json:"private"`
	HTMLURL         string   `json:"html_url"`
	License         *License `json:"license"`
}
type Handler struct {
	Client *Github.Client
}

func NewHandler(client *Github.Client) *Handler {
	return &Handler{
		Client: client,
	}
}

type GetRepositoryInput struct {
	Owner string `json:"owner"`
	Name  string `json:"name"`
}

func (h *Handler) GetRepository(ctx context.Context, req *mcp.CallToolRequest, input GetRepositoryInput) (*mcp.CallToolResult, any, error) {

	path := fmt.Sprintf("/repos/%s/%s", input.Owner, input.Name)
	body, err := h.Client.Get(ctx, path)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to get repository: %w", err)
	}
	var output RepositoryOutput
	if err := json.Unmarshal(body, &output); err != nil {
		return nil, nil, fmt.Errorf("failed to parse repository data: %w", err)
	}

	result, err := json.Marshal(output)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to build response: %w", err)
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{
				Text: string(result),
			},
		},
	}, nil, nil
}
