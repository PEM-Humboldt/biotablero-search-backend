from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric_layer" DROP CONSTRAINT IF EXISTS "uid_polygon_met_metric__146f2d";
        ALTER TABLE "polygon_metric_layer" ADD "group_name" VARCHAR(100) NOT NULL DEFAULT 'total';
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_metric__5da933" ON "polygon_metric_layer" ("metric_id", "polygon_id", "item_id", "class_id", "group_name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_polygon_met_metric__5da933";
        ALTER TABLE "polygon_metric_layer" DROP COLUMN "group_name";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_polygon_met_metric__146f2d" ON "polygon_metric_layer" ("metric_id", "polygon_id", "item_id", "class_id");"""


MODELS_STATE = (
    "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"
    "rkhHtZM7Z3n4bj5T/zqoX3"
)
