from app.models.models import Polygon, PolygonMetric
from app.persistence.polygon_metric_persistence import create_polygon_metric

from fastapi import HTTPException

from app.services.metrics import get_areas_by_polygon


async def get_or_create_polygon_metric(
    polygon_id: int, metric_id: str
) -> list:
    """
    Checks if metric values already exist for the given polygon.
    If they exist, return them.
    Otherwise, calculate them, persist them, and return the result.
    """
    polygon_obj = await Polygon.get_or_none(id=polygon_id)
    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    metric = await PolygonMetric.get_or_none(
        polygon=polygon_obj, metric=metric_id
    )
    if metric:
        return metric.values

    values = get_areas_by_polygon(metric_id, polygon_obj.geometry)

    await create_polygon_metric(polygon_obj, metric_id, values)
    return values
