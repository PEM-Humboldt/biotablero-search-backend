import sys

from app.database.populate_db import populate_db
import logging

logger = logging.getLogger(sys.modules[__name__].__package__ or __name__)


async def post_migrate():
    logger.info("Ejecutando post-migrate...")
    await populate_db()
    logger.info("Se ejecutaron los inserts correctamente")


if __name__ == "__main__":
    import asyncio

    asyncio.run(post_migrate())
