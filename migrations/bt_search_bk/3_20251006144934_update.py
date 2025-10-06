from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "collection" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "stac_url" VARCHAR(255) NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL
);
        CREATE TABLE IF NOT EXISTS "metric" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "short_name" VARCHAR(50) NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL,
    "collection_id" INT NOT NULL REFERENCES "collection" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_metric_short_n_13c43e" UNIQUE ("short_name", "name", "collection_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "collection";
        DROP TABLE IF EXISTS "metric";"""
