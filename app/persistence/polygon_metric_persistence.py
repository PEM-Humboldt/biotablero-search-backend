from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import IntegrityError
from logging import getLogger

from app.models.models import Metric, PolygonMetric, Polygon
from app.utils import context_vars
from app.utils.errors import ServerError

logger = getLogger(__name__)
request_id_context = context_vars.request_id_context


def _normalize_metric_group(metric: Metric, group: str | None) -> str:
    indicator = next(iter(metric.indicator), None)
    if indicator is not None and indicator.has_group and group:
        return group
    return "total"


async def create_polygon_metric(
    polygon: Polygon,
    metric: Metric,
    values: list | dict,
    group: str | None = None,
    db: BaseDBAsyncClient | None = None,
):
    """
    Store the computed metric values associated with a polygon.
    """
    create_kwargs = {}
    if db is not None:
        create_kwargs["using_db"] = db
    try:
        await PolygonMetric.create(
            polygon=polygon,
            metric=metric,
            values=values,
            group_name=_normalize_metric_group(metric, group),
            **create_kwargs,
        )
    except IntegrityError as e:
        raise ServerError(
            code=500,
            usr_msg="There was an error saving the metric values.",
            e=e,
        ) from e

    logger.info(
        f"PolygonMetric created for metric '{metric.name}' and polygon ID {polygon.id}",
        extra={"request_id": request_id_context.get()},
    )


async def get_polygon_metric(
    polygon_obj: Polygon,
    metric_obj: Metric,
    group: str | None = None,
    db: BaseDBAsyncClient | None = None,
) -> PolygonMetric | None:
    """
    Get Polygon metric object by polygon and metric.
    """
    query = PolygonMetric.filter(
        polygon=polygon_obj,
        metric=metric_obj,
        group_name=_normalize_metric_group(metric_obj, group),
    )
    if db is not None:
        query = query.using_db(db)
    return await query.first()
