from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "allows_national" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "allows_national";"""


MODELS_STATE = (
    "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"
)
