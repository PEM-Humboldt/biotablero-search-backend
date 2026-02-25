from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "has_layer" BOOL NOT NULL DEFAULT false;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "has_layer";"""


MODELS_STATE = (
    "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"
    "//A9vHS3o="
)
