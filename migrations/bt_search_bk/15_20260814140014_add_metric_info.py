from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "metric_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "metric_info";"""


MODELS_STATE = (
    "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"
    "/wOeC+Td"
)
