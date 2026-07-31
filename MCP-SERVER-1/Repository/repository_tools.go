package Repository

import (
	"context"
	"fmt"
	"io"
	"net/http"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type GetRepositoryInput struct {
	Owner string `json:"owner"`
	Name  string `json:"name"`
}

func GetRepository(
	ctx context.Context,
	req *mcp.CallToolRequest,
	input GetRepositoryInput,
) (*mcp.CallToolResult, any, error) {
	// make the structure of the url make a Get request create http client send the request using http client

	url := fmt.Sprintf(
		"https://api.github.com/repos/%s/%s",
		input.Owner,
		input.Name,
	) // making the url https://api.github.com/repos/aziz/Hello-World

	httpReq, err := http.NewRequestWithContext(
		ctx,
		http.MethodGet,
		url,
		nil,
	)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create request: %v", err)
	}

	client := &http.Client{} // the object responsible of making http requests

	resp, err := client.Do(httpReq)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, nil, fmt.Errorf("failed to create request: %v", err)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create request: %v", err)
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{
				Text: string(body),
			},
		},
	}, nil, nil
}
