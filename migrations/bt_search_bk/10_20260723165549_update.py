from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" ADD "category" VARCHAR(150) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" DROP COLUMN "category";"""


MODELS_STATE = (
    "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"
    "sfctA8fr/2TKlVk="
)
