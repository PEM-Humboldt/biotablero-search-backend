from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "collection_layer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "value" INT NOT NULL,
    "layer_url" VARCHAR(255) NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "collection_id" INT NOT NULL REFERENCES "collection" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "collection_layer";"""


MODELS_STATE = (
    "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"
)
