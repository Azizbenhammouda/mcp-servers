package main

import (
	"context"
	"log"
	"os"

	"github.com/Azizbenhammouda/MCP-SERVERS/MCP-SERVER-1/Github"
	"github.com/Azizbenhammouda/MCP-SERVERS/MCP-SERVER-1/Repository"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func main() {
	token := os.Getenv("GITHUB_TOKEN")
	if token == "" {
		log.Fatal("GITHUB_TOKEN environment variable is required")
	}

	client := Github.NewClient(token)
	handler := Repository.NewHandler(client)

	server := mcp.NewServer(&mcp.Implementation{
		Name:    "Github Server",
		Version: "1.0.0",
	}, nil)

	mcp.AddTool(server, &mcp.Tool{
		Description: "Get information about a GitHub repository",
		Name:        "get_repository",
	}, handler.GetRepository)

	err := server.Run(context.Background(), &mcp.StdioTransport{})
	if err != nil {
		log.Fatal(err)
	}
}
