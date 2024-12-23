from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "polygons" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "polygon_geometry" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "metricpolygons" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "metric_name" VARCHAR(100) NOT NULL,
    "values" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygons" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "metricpolygonsitems" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "raster_data" BYTEA,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "metric_polygon_id" INT NOT NULL REFERENCES "metricpolygons" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "precalculatedareas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "area_id" VARCHAR(100) NOT NULL,
    "area_type" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygons" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
