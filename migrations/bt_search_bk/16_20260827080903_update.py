from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric_collection" ADD "group_name" VARCHAR(100);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric_collection" DROP COLUMN "group_name";"""


MODELS_STATE = (
    "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"
)
