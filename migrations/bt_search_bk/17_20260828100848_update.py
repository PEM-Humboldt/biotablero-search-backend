from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric_item" DROP CONSTRAINT IF EXISTS "uid_polygon_met_metric__146f2d";
        ALTER TABLE "polygon_metric_item" ADD "group_name" VARCHAR(100) NOT NULL DEFAULT 'total';
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_metric__efc63e" ON "polygon_metric_item" ("metric_id", "polygon_id", "item_id", "class_id", "group_name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_metric__efc63e";
        ALTER TABLE "polygon_metric_item" DROP COLUMN "group_name";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_metric__146f2d" ON "polygon_metric_item" ("metric_id", "polygon_id", "item_id", "class_id");"""


MODELS_STATE = (
    "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"
    "=="
)
