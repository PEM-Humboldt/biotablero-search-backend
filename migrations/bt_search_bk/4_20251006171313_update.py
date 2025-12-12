from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """        
        ALTER TABLE "polygon_metric" ADD "metric_id" INT NOT NULL;
        ALTER TABLE "polygon_metric" DROP COLUMN "metric";
        ALTER TABLE "polygon_metric_item" ADD "metric_id" INT NOT NULL;
        ALTER TABLE "polygon_metric_item" DROP COLUMN "metric";
        ALTER TABLE "polygon_metric" ADD CONSTRAINT "fk_polygon__metric_b9639c48" FOREIGN KEY ("metric_id") REFERENCES "metric" ("id") ON DELETE CASCADE;
        ALTER TABLE "polygon_metric_item" ADD CONSTRAINT "fk_polygon__metric_684eb6e6" FOREIGN KEY ("metric_id") REFERENCES "metric" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric_item" DROP CONSTRAINT "fk_polygon__metric_684eb6e6";
        ALTER TABLE "polygon_metric" DROP CONSTRAINT "fk_polygon__metric_b9639c48";
        ALTER TABLE "polygon_metric" ADD "metric" VARCHAR(100) NOT NULL;
        ALTER TABLE "polygon_metric" DROP COLUMN "metric_id";
        ALTER TABLE "polygon_metric_item" ADD "metric" VARCHAR(100) NOT NULL;
        ALTER TABLE "polygon_metric_item" DROP COLUMN "metric_id";"""
