from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "has_layer";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "has_layer" BOOL NOT NULL;"""


MODELS_STATE = (
    "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"
)
