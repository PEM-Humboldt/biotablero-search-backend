
CREATE EXTENSION IF NOT EXISTS plpgsql;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;


CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_raster;


DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I SET postgis.gdal_enabled_drivers = ''ENABLE_ALL''', current_database());
    EXECUTE format('ALTER DATABASE %I SET postgis.enable_outdb_rasters = true', current_database());
END $$;
