import hashlib
import json
from app.utils.config import get_settings
import logging
from tortoise.exceptions import DoesNotExist

from app.utils.config import TORTOISE_ORM
from tortoise import Tortoise
from app.models.models import Polygon, AreaType
import asyncio


settings = get_settings()
settings.configure_logging()

logger = logging.getLogger(__name__)

DEFAULT_UNKNOWN_VALUE = "Desconocido"


async def get_area_type(area_name: str):
    try:
        return await AreaType.get(id=area_name)
    except DoesNotExist:
        return await AreaType.create(id=area_name)


def generate_hash(geometry):
    return hashlib.sha256(
        json.dumps(geometry, sort_keys=True).encode()
    ).hexdigest()


async def insert_states_from_geojson(area_type, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    area_type_obj = await get_area_type(area_type)

    polygon_name = "name"
    # states
    if area_type == "states":
        polygon_name = "dpto_cnmbr"
    # sa ()
    elif area_type == "sa":
        polygon_name = "nombre"
    # basinSubzones
    elif area_type == "basinSubzones":
        polygon_name = "nom_szh"

    polygons = []
    for feature in data["features"]:
        geometry = feature.get("geometry", None)
        if not geometry:
            continue
        
        area = feature["properties"].get("shape_Area", 0)
        name = feature["properties"].get(polygon_name, DEFAULT_UNKNOWN_VALUE)

        polygon = Polygon(
            hash=generate_hash(str(geometry)),
            geometry=geometry,
            area_type=area_type_obj,
            name=name,
            area=area,
        )
        polygons.append(polygon)
    
    if polygons:
        await Polygon.bulk_create(polygons)
        logger.info(
            f"✔ {len(polygons)} polígonos insertados en la BD",
            extra={"request_id": "N/A"},
        )
    else:
        logger.info(
            "⚠ No se insertaron polígonos. Verifica el archivo GeoJSON.",
            extra={"request_id": "N/A"},
        )    


async def run():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    await insert_states_from_geojson("states", "data/departamentos.geojson")
    await insert_states_from_geojson("ea", "data/jurisdicciones-ambientales.geojson")
    await insert_states_from_geojson("basinSubzones", "data/subzonas-hidrograficas.geojson")
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(run())
