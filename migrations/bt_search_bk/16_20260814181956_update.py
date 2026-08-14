from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "collection_layer" ADD "bbox" JSONB NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "collection_layer" DROP COLUMN "bbox";"""


MODELS_STATE = (
    "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"
)
