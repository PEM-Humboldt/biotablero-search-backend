from tortoise.transactions import in_transaction
from logging import getLogger

from app.models.models import Metric, PolygonMetric, Polygon
from app.utils import context_vars


logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


async def create_polygon_metric(
    polygon: Polygon, metric: Metric, values: list | dict
):
    """
    Store the computed metric values associated with a polygon.
    """
    async with in_transaction():
        await PolygonMetric.create(
            polygon=polygon,
            metric=metric,
            values=values,
        )

        logger.info(
            f"PolygonMetric created for metric '{metric.name}' and polygon ID {polygon.id}",
            extra={"request_id": request_id_context.get()},
        )
