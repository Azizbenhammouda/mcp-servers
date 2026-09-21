package main

import (
	"context"
	"log"

	"github.com/Azizbenhammouda/mcp-servers/MCP-SERVER-3/tools"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

func main() {
	server := mcp.NewServer(&mcp.Implementation{Name: "sqlite-mcp-server"}, nil)
	server.AddTool(&mcp.Tool{
		Name:        "list_tables",
		Description: "Lists all tables in the store database. Call this first to see what data is available, then use describe_table for column details.",
	}, tools.List_tables)
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		log.Fatalf("Server failure: %v", err)

	}
}
