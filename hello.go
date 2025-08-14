package main

import (
	"context"
	"database/sql"
	_ "embed"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/snowflakedb/gosnowflake"
)

//go:embed insert.sql
var insert string

//go:embed query.sql
var query string

//go:embed put.sql
var put string

//go:embed merge.sql
var merge string

func main() {
	fmt.Println("Hello, World!")

	conf := &gosnowflake.Config{
		Account:  "test",
		User:     "test",
		Password: "test",
		Database: "test",
		Host:     "snowflake.localhost.localstack.cloud",
		Port:     4567,
		Schema:   "MYSCHEMA",
	}
	connector, err := gosnowflake.DSN(conf)
	if err != nil {
		fmt.Printf("Failed to create DSN: %v\n", err)
		return
	}
	db, err := sql.Open("snowflake", connector)
	if err != nil {
		fmt.Printf("Failed to open database: %v\n", err)
		return
	}
	if err := db.Ping(); err != nil {
		fmt.Printf("Failed to connect to Snowflake: %v\n", err)
		return
	}
	fmt.Println("Successfully connected to Snowflake!")

	tx, err := db.Begin()
	if err != nil {
		fmt.Printf("Failed to begin transaction: %v\n", err)
		return
	}
	ctx := context.Background()
	_, err = tx.ExecContext(ctx, insert)
	if err != nil {
		fmt.Printf("Failed to execute insert statement: %v\n", err)
		return
	}
	fmt.Println("Insert statement executed successfully!")
	dir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Failed to get current working directory: %v\n", err)
		return
	}
	filePath := filepath.Join(dir, "test.csv")
	put = strings.ReplaceAll(put, "[LOCAL_PATH]", filePath)
	_, err = tx.ExecContext(ctx, put)
	if err != nil {
		fmt.Printf("Failed to execute put statement: %v\n", err)
		tx.Rollback()
		return
	}
	fmt.Println("Put statement executed successfully!")
	_, err = tx.ExecContext(ctx, merge)
	if err != nil {
		fmt.Printf("Failed to execute merge statement: %v\n", err)
		tx.Rollback()
		return
	}
	fmt.Println("Merge statement executed successfully!")
	rows, err := tx.QueryContext(ctx, query)
	if err != nil {
		fmt.Printf("Failed to execute query: %v\n", err)
		tx.Rollback()
		return
	}
	defer rows.Close()
	/*for rows.Next() {
		var col1 string
		var col2 int
		if err := rows.Scan(&col1, &col2); err != nil {
			fmt.Printf("Failed to scan row: %v\n", err)
			return
		}
		fmt.Printf("Row: %s, %d\n", col1, col2)
	}*/
	if err := rows.Err(); err != nil {
		fmt.Printf("Error during row iteration: %v\n", err)
		tx.Rollback()
		return
	}
	fmt.Println("Query executed successfully!")
	if err := tx.Commit(); err != nil {
		fmt.Printf("Failed to commit transaction: %v\n", err)
		return
	}
	if err := db.Close(); err != nil {
		fmt.Printf("Failed to close database: %v\n", err)
		return
	}
	fmt.Println("Database connection closed successfully!")
	fmt.Println("Goodbye, World!")
}
