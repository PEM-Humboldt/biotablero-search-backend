from typing import Optional

from tortoise.transactions import in_transaction
from app.models.models import Polygon, AreaType
from logging import getLogger


from app.routes.schemas.PolygonRequest import PolygonGeometry
from app.utils import context_vars
from app.utils.polygon_utils import generate_hash, get_polygon_area_ha

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def get_polygon(polygon: PolygonGeometry) -> Optional[int]:
    """
    Check if a polygon exists in the DB by hash. Return its ID if it exists.
    """
    hash_value = generate_hash(polygon)
    polygon_obj = await Polygon.get_or_none(hash=hash_value)
    if polygon_obj:
        logger.info(
            "Polygon already exists in the database.",
            extra={"request_id": request_id_context.get()},
        )
        return polygon_obj.id
    return None


async def create_polygon(polygon: PolygonGeometry) -> int:
    """
    Create a new polygon in the DB .
    """
    hash_value = generate_hash(polygon)
    area_ha = get_polygon_area_ha(polygon)

    async with in_transaction():
        area_type = await AreaType.get(id="custom")
        polygon_obj = await Polygon.create(
            hash=hash_value,
            geometry=polygon.model_dump(),
            name="Polígono",
            area=area_ha,
            area_type=area_type,
        )

        logger.info(
            "Polygon inserted into the database.",
            extra={"request_id": request_id_context.get()},
        )

    return polygon_obj.id
