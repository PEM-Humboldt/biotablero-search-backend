from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygons" ADD "polygon_hash" VARCHAR(64)  UNIQUE;
        CREATE INDEX "idx_polygons_polygon_2e7193" ON "polygons" ("polygon_hash");
        CREATE UNIQUE INDEX "uid_polygons_polygon_2e7193" ON "polygons" ("polygon_hash");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_polygons_polygon_2e7193";
        DROP INDEX "idx_polygons_polygon_2e7193";
        ALTER TABLE "polygons" DROP COLUMN "polygon_hash";"""
