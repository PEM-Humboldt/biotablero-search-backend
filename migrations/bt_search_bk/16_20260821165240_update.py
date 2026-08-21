from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_59bbb7";
        ALTER TABLE "metric_collection" ADD "group_name" VARCHAR(100);
        ALTER TABLE "polygon_metric" ADD "group_name" VARCHAR(100);
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_3b3c9b" ON "polygon_metric" ("polygon_id", "metric_id", "group_name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_3b3c9b";
        ALTER TABLE "species_stats" ADD "date" DATE NOT NULL;
        ALTER TABLE "species_stats" RENAME COLUMN "group_name" TO "group";
        ALTER TABLE "polygon_metric" DROP COLUMN "group_name";
        ALTER TABLE "metric_collection" DROP COLUMN "group_name";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_59bbb7" ON "polygon_metric" ("polygon_id", "metric_id");"""


MODELS_STATE = (
    "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"
)
