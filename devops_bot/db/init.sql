CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    number VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS email (
    id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL
);
