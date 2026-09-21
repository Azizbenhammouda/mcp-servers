package tools

import (
	"context"
	"database/sql"
	"fmt"
	"os"
	"strings"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	_ "modernc.org/sqlite"
)

func Connect_db() (*sql.DB, error) {
	path := os.Getenv("STORE_DB_PATH")
	if path == "" {
		return nil, fmt.Errorf("STORE_DB_PATH is not set")
	}
	if _, err := os.Stat(path); err != nil {
		return nil, err
	}
	db, err := sql.Open("sqlite", path)
	if err != nil {
		return nil, err
	}
	err = db.Ping()
	if err != nil {
		return nil, err
	}
	return db, nil
}

type args struct{}

func List_tables(ctx context.Context, req *mcp.CallToolRequest, ar args) (*mcp.CallToolResult, any, error) {
	db, err := Connect_db()
	if err != nil {
		return nil, nil, err
	}
	defer db.Close()
	query := `
	SELECT name
	FROM sqlite_master
	WHERE type= 'table'
	`
	rows, err := db.Query(query)
	if err != nil {
		return nil, nil, err
	}
	result := []string{}
	defer rows.Close()
	for rows.Next() {
		var name string
		err := rows.Scan(&name)
		if err != nil {
			return nil, nil, err
		}
		result = append(result, name)
	}
	if err := rows.Err(); err != nil {
		return nil, nil, err
	}
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: strings.Join(result, "\n")},
		},
	}, nil, nil
}
