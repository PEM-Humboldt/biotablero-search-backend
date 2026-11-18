from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" ADD "collection_id" INT NOT NULL;
        ALTER TABLE "dpc" ADD CONSTRAINT "fk_dpc_collecti_5865ee89" FOREIGN KEY ("collection_id") REFERENCES "collection" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "dpc" DROP CONSTRAINT IF EXISTS "fk_dpc_collecti_5865ee89";
        ALTER TABLE "dpc" DROP COLUMN "collection_id";"""


MODELS_STATE = (
    "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"
    "Ck/N0ZGBPYniFNcsLtGQ6aSXj9D5E1WC4="
)
