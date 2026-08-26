from tortoise import BaseDBAsyncClient


RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric"
        ADD COLUMN IF NOT EXISTS "group" VARCHAR(100) NOT NULL DEFAULT 'total';
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_59bbb7";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_group"
        ON "polygon_metric" ("polygon_id", "metric_id", "group");
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_polygon_group";
        ALTER TABLE "polygon_metric" DROP COLUMN IF EXISTS "group";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_polygon_59bbb7"
        ON "polygon_metric" ("polygon_id", "metric_id");
    """
