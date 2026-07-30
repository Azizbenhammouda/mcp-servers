package main

import (
	"context"
	"log"

	"github.com/Azizbenhammouda/MCP-SERVERS/MCP-SERVER-1/Repository"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func main() {
	server := mcp.NewServer(&mcp.Implementation{
		Name:    "Github Server",
		Version: "1.0.0",
	}, nil)
	mcp.AddTool(server, &mcp.Tool{
		Description: "Get information about a GitHub repository",
		Name:        "get_repository",
	}, Repository.GetRepository)
	err := server.Run(context.Background(), &mcp.StdioTransport{})
	if err != nil {
		log.Fatal(err)
	}
}
