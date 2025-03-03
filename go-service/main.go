package main

import (
	"fmt"

	"github.com/SethGK/RefRangeHub/go-service/internal/db"
)

func main() {
	// Initialize DB
	db.InitDB()

	// Run Migrations
	db.RunMigrations()

	// Optionally, run some queries to test the setup
	fmt.Println("Database setup is complete.")

	// Close DB connection
	db.CloseDB()
}
