package main

import (
	"context"
	"log"
	"os"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type SendNotificationInput struct {
	To      string `json:"to" jsonschema:"recipient phone number in E.164 format, e.g. +911234567890"`
	Message string `json:"message" jsonschema:"the full notification text to send"`
}

func requireEnv(key string) string {
	val := os.Getenv(key)
	if val == "" {
		log.Fatalf("missing required env var: %s", key)
	}
	return val
}

func main() {
	token := requireEnv("WHATSAPP_TOKEN")
	phoneNumberID := requireEnv("WHATSAPP_PHONE_NUMBER_ID")
	templateName := requireEnv("WHATSAPP_TEMPLATE_NAME")

	_ = token
	_ = phoneNumberID
	_ = templateName
	server := mcp.NewServer(&mcp.Implementation{
		Name:    "WhatsAppServer",
		Version: "1.0.0",
	}, nil)
	err := server.Run(context.Background(), &mcp.StdioTransport{})
	if err != nil {
		log.Fatalf("Server failure %v", err)
	}
}
