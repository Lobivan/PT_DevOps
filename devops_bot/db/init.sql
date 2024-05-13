create user replicator with ${DB_REPL_USER} encrypted password '${DB_REPL_PASSWORD}';
select pg_create_physical_replication_slot('replication_slot');

ALTER ROLE postgres WITH PASSWORD '${DB_PASSWORD}';

CREATE DATABASE ${DB_DATABASE};
\c ${DB_DATABASE}

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    number VARCHAR(100) NOT NULL
)

CREATE TABLE IF NOT EXISTS email (
    id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL
)