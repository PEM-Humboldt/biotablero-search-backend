import logging
import asyncio
from argparse import ArgumentParser
from tortoise import Tortoise

from database.seed_area_types import seed_area_types
from database.seed_collections_and_metrics import seed_collections_and_metrics
from database.seed_connectivity_indicators import seed_connectivity_indicators
from database.seed_polygons import seed_polygons

from app.utils.config import get_settings, TORTOISE_ORM

settings = get_settings()

logger = logging.getLogger(__name__)


async def populate_db(which_set="all"):
    logger.info("Iniciando inserción de datos...", extra={"request_id": "N/A"})
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    try:
        match which_set:
            case "all":
                await seed_area_types()
                await seed_polygons()
                await seed_collections_and_metrics()
                await seed_connectivity_indicators()
            case "areas":
                await seed_area_types()
                await seed_polygons()
            case "indicators":
                await seed_connectivity_indicators()
            case "metrics":
                await seed_collections_and_metrics()
    except Exception as e:
        print(e)

    await Tortoise.close_connections()
    logger.info(
        "La conexión a la base de datos ha sido cerrada",
        extra={"request_id": "N/A"},
    )


if __name__ == "__main__":
    settings.configure_logging()

    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--sets",
        dest="which_set",
        help="Especifica que conjunto de datos poblar, opciones: 'all', 'areas', 'metrics', 'indicators",
        default="all",
        required=False,
    )

    args = parser.parse_args()

    asyncio.run(populate_db(args.which_set))
