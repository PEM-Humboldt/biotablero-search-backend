# Database Migration System with Alembic and Docker

This document provides instructions for setting up and managing database migrations in the `biotablero-search-backend` project using Alembic in a Docker environment. It includes the purpose of `init_postgis.sql` and essential Alembic commands.

## Setup and Configuration

### Environment Configuration

Before running the Docker setup, create a `.env` file in the project root to configure your database credentials. Alembic and other components require these environment variables for proper functionality.

Here is an example of the `.env` file:

```text
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name

DATABASE_URL_SYNC=postgresql://your_postgres_user:your_postgres_password@localhost/your_database_name
DATABASE_URL_ASYNC=postgresql+asyncpg://your_postgres_user:your_postgres_password@localhost/your_database_name
```

* Replace `your_postgres_user`, `your_postgres_password`, and `your_database_name` with the credentials you choose.
* These values will be used by Docker and Alembic to connect to the PostgreSQL database.

---

1. ****Step 1:** Docker Build and Start-up**
Build Docker Containers: Use the following command to build Docker containers without using cached versions:

```bash
docker-compose build --no-cache
```
This command ensures that all components, including dependencies, are freshly built.

2. Start Containers in Detached Mode:

```bash
docker-compose up -d
```

This initializes the containers in the background. The configuration specified in docker-compose.yml will set up both the database and the application, with the database container configured to include PostGIS extensions.

## Database Initialization with init_postgis.sql

The `init_postgis.sql` script is used for setting up the PostGIS environment in the PostgreSQL database. Here’s a breakdown of what this script does:

* **Enable Procedural Language Support (plpgsql):**

```sql
CREATE EXTENSION IF NOT EXISTS plpgsql;
```
This command enables PostgreSQL's procedural language, allowing functions written in PL/pgSQL, a core language for stored procedures.

**Install Additional Extensions:**

* **fuzzystrmatch:** Provides functions for approximate string matching, useful for text comparisons.

* **postgis:** Installs PostGIS, which extends PostgreSQL to handle geographic objects, making it suitable for geospatial analysis.

* **postgis_raster:** Adds support for raster data (gridded data) in PostGIS.

```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_raster;
```

* **Enable GDAL Drivers and External Raster Support:**

```sql
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I SET postgis.gdal_enabled_drivers = ''ENABLE_ALL''', current_database());
    EXECUTE format('ALTER DATABASE %I SET postgis.enable_outdb_rasters = true', current_database());
END $$;
```

These commands configure the database to use GDAL drivers (libraries for geospatial data) and enable storage of raster files outside the database, optimizing for large datasets.

## Step 3: Setting Up Alembic for Migrations

1. **Initialize Alembic:**

* If no migrations exist, run:

```bash
alembic init
```
* This command sets up Alembic's basic directory structure in a migrations folder.

2. **Generate Migration Revisions:**

* To track changes in the database models, create migration files automatically with:
    
    ```bash
    alembic revision --autogenerate -m "migration message"
    ```
  
3. **Apply Migrations to the Database:**

* Use the following command to apply the latest migrations to the database:
    
    ```bash
    alembic upgrade head
    ```
  
* This command will bring the database schema up to date with the latest migration version.


## Common Alembic Commands

Here are a few helpful Alembic commands for managing migrations:

* View Current Database Migration Version:

```bash
alembic current
```
Displays the current migration version applied in the database.

* Rollback to Previous Version:

```bash
alembic downgrade -1
```
Rolls back the database by one migration step. Replace -1 with a specific version if needed.

* Generate a Migration Script Manually:

```bash
alembic revision -m "description of change"
```
This command creates a new revision file where changes can be specified manually.

* Show the List of Migrations:

```bash
alembic history
```

## Potential Errors and Troubleshooting

* Missing Environment Variables: Ensure that environment variables (e.g., DATABASE_URL_SYNC) are properly set, as missing variables will lead to connection issues.

* PostGIS Extensions Not Enabled: If errors arise with PostGIS functions, verify that init_postgis.sql has been executed correctly to enable the necessary extensions.

* Permission Errors with Docker Volumes: If Docker is unable to access or write to the volume directories, ensure that permissions are set correctly on your host machine.

*authors*
* [Juan Zambrano](mailto:jzambrano@humboldt.org.co)
