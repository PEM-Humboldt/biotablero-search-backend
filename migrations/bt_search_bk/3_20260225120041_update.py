from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "polygon_metric_item";
        CREATE TABLE IF NOT EXISTS "polygon_metric_item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "class_id" VARCHAR(100) NOT NULL,
    "item_id" VARCHAR(100) NOT NULL,
    "layer_url" VARCHAR(255) NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_polygon_met_metric__146f2d" UNIQUE ("metric_id", "polygon_id", "item_id", "class_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "polygon_metric_item";"""


MODELS_STATE = (
    "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"
)
