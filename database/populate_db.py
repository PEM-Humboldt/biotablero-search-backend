import logging
from tortoise import Tortoise

from database.seed_area_types import seed_area_types
from database.seed_collections_and_metrics import seed_collections_and_metrics
from database.insert_polygons import seed_polygons

from app.utils.config import get_settings, TORTOISE_ORM

settings = get_settings()
settings.configure_logging()

logger = logging.getLogger(__name__)


async def populate_db():
    logger.info("Ejecutando post-migrate...", extra={"request_id": "N/A"})
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    try:
        await seed_area_types()
        await seed_polygons()
        await seed_collections_and_metrics()
    except Exception as e:
        print(e)

    await Tortoise.close_connections()
    logger.info(
        "Se ejecutaron los inserts correctamente", extra={"request_id": "N/A"}
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(populate_db())
