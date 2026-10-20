from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "edges" JSONB;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "edges";"""


MODELS_STATE = (
    "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"
)
