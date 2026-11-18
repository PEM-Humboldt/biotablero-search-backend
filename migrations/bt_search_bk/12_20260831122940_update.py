from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "collection" ADD "allows_layer" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "collection" DROP COLUMN "allows_layer";"""


MODELS_STATE = (
    "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"
    "g537tPx/H8H+XPHDU="
)
