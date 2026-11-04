from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "report_data" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "creation_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_name" VARCHAR(75) NOT NULL,
    "description" VARCHAR(500) NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "report_data";"""


MODELS_STATE = (
    "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"
    "zPkCU50fYMB80kvPwH/w8qVw=="
)
