import sys

from app.utils.config import init_tortoise
import logging

logger = logging.getLogger(sys.modules[__name__].__package__ or __name__)


async def post_migrate():
    logger.info("Ejecutando post-migrate...")
    await init_tortoise()
    logger.info(
        "Se ejecutaron los inserts correctamente"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(post_migrate())