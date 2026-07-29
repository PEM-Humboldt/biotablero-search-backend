from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "species_stats" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "geofence_type" VARCHAR(50) NOT NULL,
    "date" DATE NOT NULL,
    "region_slug" VARCHAR(100) NOT NULL,
    "region_code" VARCHAR(20),
    "group_slug" VARCHAR(100) NOT NULL,
    "total" INT NOT NULL,
    "threatened_total" INT NOT NULL,
    "threatened_cr" INT NOT NULL,
    "threatened_en" INT NOT NULL,
    "threatened_vu" INT NOT NULL,
    "invasive" INT NOT NULL,
    "endemic" INT NOT NULL,
    "endemic_threatened" INT NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "polygon_id" INT NOT NULL REFERENCES "polygon" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "species_stats";"""


MODELS_STATE = (
    "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"
    "VIlA=="
)
