from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "dpc" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "dpc" DOUBLE PRECISION NOT NULL,
    "pa_id" INT NOT NULL,
    "pa_name" VARCHAR(100) NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "metric_indicator" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "indicator" VARCHAR(100) NOT NULL UNIQUE,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "metric_id" INT NOT NULL REFERENCES "metric" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "prot_conn" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "prot" DOUBLE PRECISION NOT NULL,
    "unprot" DOUBLE PRECISION NOT NULL,
    "prot_conn" DOUBLE PRECISION NOT NULL,
    "prot_unconn" DOUBLE PRECISION NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "dpc";
        DROP TABLE IF EXISTS "metric_indicator";
        DROP TABLE IF EXISTS "prot_conn";"""


MODELS_STATE = (
    "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"
    "Ti42OSCZwfS5Oc6PxYJvYeMnC8/A87O80a"
)
