from database.populate_db import populate_db
import logging
from app.utils.config import get_settings

settings = get_settings()
settings.configure_logging()

logger = logging.getLogger(__name__)


async def post_migrate():
    logger.info("Ejecutando post-migrate...", extra={"request_id": "N/A"})
    await populate_db()
    logger.info(
        "Se ejecutaron los inserts correctamente", extra={"request_id": "N/A"}
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(post_migrate())
