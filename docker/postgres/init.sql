-- Create role safely
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_roles WHERE rolname = 'health_user'
   ) THEN
      CREATE ROLE health_user LOGIN PASSWORD 'Health_xyz_123';
   END IF;
END
$$;

-- Create schema owned by health_user
CREATE SCHEMA IF NOT EXISTS health AUTHORIZATION health_user;

-- Tables

CREATE TABLE IF NOT EXISTS health.heart (
    "timestamp" TIMESTAMP NULL,
    bpm BIGINT NULL,
    "date" DATE NULL
);

CREATE TABLE IF NOT EXISTS health.sleep (
    "start_timestamp" TIMESTAMP NULL,
    "end_timestamp" TIMESTAMP NULL,
    value TEXT NULL,
    hours DOUBLE PRECISION NULL,
    "date" DATE NULL
);


CREATE TABLE IF NOT EXISTS health.steps (
    "start_timestamp" TIMESTAMP NULL,
     "end_timestamp" TIMESTAMP NULL,
    steps BIGINT NULL,
    "date" DATE NULL
);