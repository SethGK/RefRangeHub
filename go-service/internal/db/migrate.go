package db

import (
	"log"

	"github.com/golang-migrate/migrate/v4"
	"github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
)

func RunMigrations() {
	// Open the PostgreSQL database connection
	db, err := DB.DB()
	if err != nil {
		log.Fatalf("Error getting DB instance: %v", err)
	}

	// Create a new database driver
	driver, err := postgres.WithInstance(db, &postgres.Config{})
	if err != nil {
		log.Fatalf("Error creating database driver: %v", err)
	}

	// Create the migration instance (No need for `file.New`)
	m, err := migrate.NewWithDatabaseInstance(
		"file://internal/db/migrations", // Ensure the path is correct
		"postgres", driver,
	)
	if err != nil {
		log.Fatalf("Error creating migration instance: %v", err)
	}

	// Run migrations
	err = m.Up()
	if err != nil && err != migrate.ErrNoChange {
		log.Fatalf("Error applying migrations: %v", err)
	}

	log.Println("Migrations applied successfully!")
}
