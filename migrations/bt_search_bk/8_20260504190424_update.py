from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" ALTER COLUMN "pa_name" TYPE VARCHAR(150) USING "pa_name"::VARCHAR(150);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" ALTER COLUMN "pa_name" TYPE VARCHAR(100) USING "pa_name"::VARCHAR(100);"""


MODELS_STATE = (
    "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"
)
