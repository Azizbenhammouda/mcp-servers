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
		Description: "we trying things out",
		Name:        "dummytool",
	}, Repository.Ping)
	err := server.Run(context.Background(), &mcp.StdioTransport{})
	if err != nil {
		log.Fatal(err)
	}
}
