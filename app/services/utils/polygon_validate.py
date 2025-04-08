import json
import hashlib
from typing import List, Dict, Any

from tortoise.transactions import in_transaction
from app.models.models import Polygon, AreaType, PolygonMetric
from logging import getLogger

from app.routes.schemas.MetricResponse import (
    MetricResponse,
    LossPersistenceResponse,
)
from app.routes.schemas.PolygonRequest import PolygonGeometry
from app.utils import context_vars

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


def serialize_area_data(data: List[MetricResponse]) -> List[Dict[str, Any]]:
    serialized = []
    for item in data:
        if isinstance(item, LossPersistenceResponse):
            serialized.append(item.model_dump())
        elif isinstance(item, dict):
            serialized.append(item)
        else:
            logger.error(
                f"Unsupported type in MetricResponse list: {type(item)}",
                extra={"request_id": request_id_context.get()},
            )
    return serialized


def generate_hash(polygon: PolygonGeometry, name: str) -> str:
    """Generates a unique hash based on the geometry and name of the metric."""
    data = json.dumps(polygon.model_dump(), sort_keys=True) + name
    return hashlib.sha256(data.encode()).hexdigest()


"""TO DO:Validate a Way to Calculate the Total Area from the Request Polygon"""


def extract_total_area_from_last_period(area_data: list[dict]) -> float:
    sorted_data = sorted(
        area_data, key=lambda x: x["periodo"].split("-")[1], reverse=True
    )
    last_period = sorted_data[0]

    return (
        last_period.get("perdida", 0)
        + last_period.get("persistencia", 0)
        + last_period.get("no_bosque", 0)
    )


async def get_or_create_polygon(
    polygon: PolygonGeometry,
    name: str,
    area: float,
    values: List[Dict[str, Any]],
) -> int:
    """Search for a polygon by its hash and create it if it doesn't exist. The ID returns."""
    hash_value = generate_hash(polygon, name)

    async with in_transaction():
        polygon_obj = await Polygon.get_or_none(hash=hash_value)
        if polygon_obj:
            logger.info(
                "Polygon already exists in the database.",
                extra={"request_id": request_id_context.get()},
            )
        else:
            area_type = await AreaType.get(id="custom")
            polygon_obj = await Polygon.create(
                hash=hash_value,
                geometry=polygon.model_dump(),
                name=name,
                area=area,
                area_type=area_type,
            )
            logger.info(
                "Polygon inserted into the database.",
                extra={"request_id": request_id_context.get()},
            )

            await PolygonMetric.create(
                metric=name,
                values=values,
                polygon=polygon_obj,
            )

            logger.info(
                "Polygon metrics inserted.",
                extra={"request_id": request_id_context.get()},
            )

    return polygon_obj.id
