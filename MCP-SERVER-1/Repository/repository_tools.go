package Repository

import (
	"context"
	"fmt"

	"github.com/Azizbenhammouda/MCP-SERVERS/MCP-SERVER-1/Github"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

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

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{
				Text: string(body),
			},
		},
	}, nil, nil
}
