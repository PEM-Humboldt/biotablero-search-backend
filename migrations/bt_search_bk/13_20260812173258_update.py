from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "species_stats" RENAME COLUMN "group_slug" TO "group_name";
        ALTER TABLE "species_stats" DROP COLUMN IF EXISTS "geofence_type";
        ALTER TABLE "species_stats" DROP COLUMN IF EXISTS "region_slug";
        ALTER TABLE "species_stats" DROP COLUMN IF EXISTS "region_code";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "species_stats" ADD COLUMN IF NOT EXISTS "geofence_type" VARCHAR(50) NOT NULL DEFAULT '';
        ALTER TABLE "species_stats" ADD COLUMN IF NOT EXISTS "region_slug" VARCHAR(100) NOT NULL DEFAULT '';
        ALTER TABLE "species_stats" ADD COLUMN IF NOT EXISTS "region_code" VARCHAR(20);
        ALTER TABLE "species_stats" RENAME COLUMN "group" TO "group_slug";"""


MODELS_STATE = (
    "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"
)
