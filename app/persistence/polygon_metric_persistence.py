from tortoise.transactions import in_transaction
from logging import getLogger

from app.models.models import Metric, PolygonMetric, Polygon
from app.utils import context_vars


logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def create_polygon_metric(
    polygon_obj: Polygon, metric_obj: Metric, values: list
):
    """
    Store the computed metric values associated with a polygon.
    """
    async with in_transaction():
        await PolygonMetric.create(
            polygon=polygon_obj,
            metric=metric_obj,
            values=values,
        )

        logger.info(
            f"PolygonMetric created for metric '{metric_obj.short_name}' and polygon ID {polygon_obj.id}",
            extra={"request_id": request_id_context.get()},
        )
