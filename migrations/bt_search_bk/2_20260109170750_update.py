from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "area_type" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "collection" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "metric" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "metric_collection" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "polygon" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "polygon" ALTER COLUMN "name" DROP NOT NULL;
        ALTER TABLE "polygon_metric" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "polygon_metric_item" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_area_type_label_9e16b6" ON "area_type" ("label");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "area_type" DROP CONSTRAINT IF EXISTS "area_type_label_key";
        DROP INDEX IF EXISTS "uid_area_type_label_9e16b6";
        ALTER TABLE "metric" DROP COLUMN "updated_at";
        ALTER TABLE "polygon" DROP COLUMN "updated_at";
        ALTER TABLE "polygon" ALTER COLUMN "name" SET NOT NULL;
        ALTER TABLE "area_type" DROP COLUMN "updated_at";
        ALTER TABLE "collection" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "polygon_metric" DROP COLUMN "updated_at";
        ALTER TABLE "metric_collection" DROP COLUMN "updated_at";
        ALTER TABLE "polygon_metric_item" DROP COLUMN "updated_at";"""


MODELS_STATE = (
    "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"
)
