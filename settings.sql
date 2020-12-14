-- settings.sql
CREATE DATABASE memoryze;
CREATE USER memoryzeuser
WITH PASSWORD 'memoryze';
GRANT ALL PRIVILEGES ON DATABASE memoryze TO memoryzeuser;