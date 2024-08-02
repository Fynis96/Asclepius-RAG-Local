DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT 
      FROM   pg_catalog.pg_database
      WHERE  datname = 'postgres') THEN

      CREATE DATABASE postgres;
   END IF;
END
$do$;