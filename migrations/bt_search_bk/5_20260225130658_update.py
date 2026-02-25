from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon" ALTER COLUMN "area_type_id" SET NOT NULL;
        ALTER TABLE "polygon" DROP CONSTRAINT polygon_area_type_id_fkey;
        ALTER TABLE "polygon"
        ADD CONSTRAINT polygon_area_type_id_fkey
        FOREIGN KEY (area_type_id)
        REFERENCES "area_type" ("id") ON DELETE CASCADE
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon" ALTER COLUMN "area_type_id" DROP NOT NULL;"""


MODELS_STATE = (
    "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"
)
