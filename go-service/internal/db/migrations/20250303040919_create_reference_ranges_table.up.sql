CREATE TABLE reference_ranges (
    id SERIAL PRIMARY KEY,
    test_name TEXT NOT NULL,
    min_value FLOAT NOT NULL,
    max_value FLOAT NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,  -- Chemistry, Hematology, etc.
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
