from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metricpolygons" RENAME TO "metric_polygons";
        ALTER TABLE "metricpolygonsitems" RENAME TO "metric_polygons_items";
        ALTER TABLE "polygons" ADD "polygon_hash" VARCHAR(64)  UNIQUE;
        ALTER TABLE "precalculatedareas" RENAME TO "precalculated_areas";
        CREATE INDEX "idx_polygons_polygon_2e7193" ON "polygons" ("polygon_hash");
        CREATE UNIQUE INDEX "uid_polygons_polygon_2e7193" ON "polygons" ("polygon_hash");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_polygons_polygon_2e7193";
        DROP INDEX "idx_polygons_polygon_2e7193";
        ALTER TABLE "polygons" DROP COLUMN "polygon_hash";
        ALTER TABLE "metric_polygons" RENAME TO "metricpolygons";
        ALTER TABLE "precalculated_areas" RENAME TO "precalculatedareas";
        ALTER TABLE "metric_polygons_items" RENAME TO "metricpolygonsitems";"""
