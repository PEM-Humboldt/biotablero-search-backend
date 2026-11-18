from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_59bbb7";
        CREATE TABLE IF NOT EXISTS "collection_layer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "value" INT NOT NULL,
    "layer_url" VARCHAR(255) NOT NULL,
    "bbox" JSONB NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "collection_id" INT NOT NULL REFERENCES "collection" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "metric_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "species_stats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_name" VARCHAR(100) NOT NULL,
    "total" INT NOT NULL,
    "threatened_total" INT NOT NULL,
    "threatened_cr" INT NOT NULL,
    "threatened_en" INT NOT NULL,
    "threatened_vu" INT NOT NULL,
    "invasive" INT NOT NULL,
    "endemic" INT NOT NULL,
    "endemic_threatened" INT NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);
        ALTER TABLE "metric" ADD "allows_national" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "metric_collection" ADD "group_name" VARCHAR(100);
        ALTER TABLE "metric_indicator" ADD "has_group" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "polygon_metric" ADD "group_name" VARCHAR(100) NOT NULL DEFAULT 'total';
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_3b3c9b" ON "polygon_metric" ("polygon_id", "metric_id", "group_name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_3b3c9b";
        ALTER TABLE "metric" DROP COLUMN "allows_national";
        ALTER TABLE "polygon_metric" DROP COLUMN "group_name";
        ALTER TABLE "metric_indicator" DROP COLUMN "has_group";
        ALTER TABLE "metric_collection" DROP COLUMN "group_name";
        DROP TABLE IF EXISTS "species_stats";
        DROP TABLE IF EXISTS "metric_info";
        DROP TABLE IF EXISTS "collection_layer";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_59bbb7" ON "polygon_metric" ("polygon_id", "metric_id");"""


MODELS_STATE = (
    "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"
)
