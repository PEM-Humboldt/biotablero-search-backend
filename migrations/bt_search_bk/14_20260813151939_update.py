from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "has_group" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "has_group";"""


MODELS_STATE = (
    "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"
    "lH26klOB45VJkhMdr0z53td0HC//A+iegnk="
)
