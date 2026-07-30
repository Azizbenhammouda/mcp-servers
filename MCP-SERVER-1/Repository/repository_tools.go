package Repository

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type DummyInput struct {
	Name string
}

func Ping(ctx context.Context, req *mcp.CallToolRequest, input DummyInput) (*mcp.CallToolResult, any, error) {
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: "pong"},
		},
	}, nil, nil
}
