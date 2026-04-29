import hashlib
import json
from app.utils.config import get_settings
import logging
from tortoise.exceptions import DoesNotExist

from app.models.models import Polygon, AreaType
from shapely.geometry import shape

from app.persistence.utils.polygon_utils import cast_to_multi_polygon

settings = get_settings()

logger = logging.getLogger(__name__)

DEFAULT_UNKNOWN_VALUE = "Desconocido"


async def get_area_type(area_name: str):
    """
    Retrieves an AreaType object from the database.

    Args:
        area_name (str): The ID of the AreaType to retrieve.

    Returns:
        AreaType: The AreaType object if found, otherwise creates a new one.

    Raises:
        DoesNotExist: If the AreaType does not exist and cannot be created.
    """

    try:
        return await AreaType.get(id=area_name)
    except DoesNotExist:
        return await AreaType.create(id=area_name)


def generate_hash(geometry):
    """
    Generates a SHA256 hash of a geometry object.

    Args:
        geometry (dict): The geometry object to hash.

    Returns:
        str: The hexadecimal representation of the SHA256 hash.
    """

    return hashlib.sha256(
        json.dumps(geometry, sort_keys=True).encode()
    ).hexdigest()


def add_bbox(geometry):
    """
    Adds bbox value in all polygons

    Args:
        geometry (dict): The geometry object.

    Returns:
        dict: The geometry with bbox values.
    """
    if geometry["type"] == "Polygon" or geometry["type"] == "MultiPolygon":
        geometry["bbox"] = list(shape(geometry).bounds)


async def insert_polygons_from_geojson(area_type, file_path):
    """
    Inserts polygon data from a GeoJSON file into the database.

    Args:
        area_type (str): The type of area being imported (e.g., "states", "ea", "basinSubzones").
        file_path (str): The path to the GeoJSON file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    area_type_obj = await get_area_type(area_type)

    polygon_name = "name"
    area_name = "area"
    code_field = None

    if area_type == "states":
        polygon_name = "dpto_cnmbr"
        area_name = "area_ha"
        code_field = "dpto_ccdgo"
    elif area_type == "ea":
        polygon_name = "nombre"
        area_name = "area_ha"
        code_field = "car"
    elif area_type == "basinSubzones":
        polygon_name = "nom_szh"
        area_name = "area_ha"
        code_field = "COD_SZH"
    elif area_type == "paramos":
        polygon_name = "Nombre"
        area_name = "area_ha"
        code_field = "Id"

    polygons = []
    for feature in data["features"]:
        geometry = feature.get("geometry", None)
        if not geometry:
            continue

        add_bbox(geometry)
        geometry = cast_to_multi_polygon(geometry)

        area = feature["properties"].get(area_name, 0)
        name = feature["properties"].get(polygon_name, DEFAULT_UNKNOWN_VALUE)
        official_code = (
            feature["properties"].get(code_field, None) if code_field else None
        )

        polygon = Polygon(
            hash=generate_hash(dict(geometry)),
            geometry=geometry,
            area_type=area_type_obj,
            name=name,
            area=area,
            official_code=official_code,
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


async def seed_polygons():
    """
    Inserts data from GeoJSON files.
    """

    await insert_polygons_from_geojson("states", "data/departamentos.geojson")
    await insert_polygons_from_geojson(
        "ea", "data/jurisdicciones-ambientales.geojson"
    )
    await insert_polygons_from_geojson(
        "basinSubzones", "data/subzonas-hidrograficas.geojson"
    )
    await insert_polygons_from_geojson("paramos", "data/paramos.geojson")
