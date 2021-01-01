-- settings.sql
CREATE DATABASE memoryze;
CREATE USER memoryzeuser
WITH PASSWORD 'memoryze';
GRANT ALL PRIVILEGES ON DATABASE memoryze TO memoryzeuser;

-- if you cant drop a database, execute the following sets of commands accordingly

-- 1)
-- SELECT *
-- FROM pg_stat_activity
-- WHERE datname = 'memoryze';

-- 2)
-- SELECT pg_terminate_backend (pid)
-- FROM pg_stat_activity
-- WHERE	pg_stat_activity.datname = 'memoryze';

-- then drop the database
-- DROP DATABASE memoryze