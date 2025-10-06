from tortoise import Tortoise
from database.seed_area_types import seed_area_types
from database.seed_collections_and_metrics import seed_collections_and_metrics
from database.insert_polygons import seed_polygons
from app.utils.config import TORTOISE_ORM


async def populate_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    await seed_area_types()
    await seed_collections_and_metrics()
    await seed_polygons()

    await Tortoise.close_connections()
