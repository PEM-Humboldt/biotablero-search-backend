from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "area_type" (
    "id" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "label" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "polygon" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "hash" VARCHAR(255)  UNIQUE,
    "geometry" JSONB NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "area" DOUBLE PRECISION NOT NULL,
    "area_type_id" VARCHAR(50) REFERENCES "area_type" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_polygon_hash_e7f306" ON "polygon" ("hash");
CREATE TABLE IF NOT EXISTS "polygon_metric" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "metric" VARCHAR(100) NOT NULL,
    "values" JSONB NOT NULL,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "polygon_metric_item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "metric" VARCHAR(100) NOT NULL,
    "layer_url" VARCHAR(255) NOT NULL,
    "category" INT NOT NULL,
    "item_id" VARCHAR(100) NOT NULL,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_polygon_met_metric_c667f3" UNIQUE ("metric", "category", "item_id")
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
