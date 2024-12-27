from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metricpolygons" RENAME COLUMN "metric_polygon_id" TO "id";
        ALTER TABLE "metricpolygonsitems" RENAME COLUMN "item_id" TO "id";
        ALTER TABLE "polygons" RENAME COLUMN "polygon_id" TO "id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygons" RENAME COLUMN "id" TO "polygon_id";
        ALTER TABLE "metricpolygons" RENAME COLUMN "id" TO "metric_polygon_id";
        ALTER TABLE "metricpolygonsitems" RENAME COLUMN "id" TO "item_id";"""
