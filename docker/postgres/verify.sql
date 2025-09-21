\echo 'Verifying schema and tables...'

-- Fail if schema is missing
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT 1 FROM information_schema.schemata WHERE schema_name = 'health'
   ) THEN
      RAISE EXCEPTION 'Schema "health" does not exist!';
   END IF;
END
$$;

-- Fail if any required table is missing
DO
$$
DECLARE
   missing_tables TEXT[];
BEGIN
   SELECT ARRAY(
      SELECT unnest(ARRAY['heart','heart_daily','sleep','sleep_daily','steps','steps_daily'])
      EXCEPT
      SELECT table_name FROM information_schema.tables WHERE table_schema = 'health'
   ) INTO missing_tables;

   IF array_length(missing_tables, 1) IS NOT NULL THEN
      RAISE EXCEPTION 'Missing tables in schema "health": %', missing_tables;
   END IF;
END
$$;

\echo 'Validation successful ✅'
