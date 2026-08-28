from app.models.models import Metric, PolygonMetricLayer, Polygon
from app.persistence.metric_collection_persistence import (
    normalize_metric_group,
)
from app.utils.errors import ServerError
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import IntegrityError


async def get_existing_layer(
    metric_id: Metric,
    polygon: Polygon,
    class_id: str,
    item_id: str,
    group: str | None = None,
    db: BaseDBAsyncClient | None = None,
):
    query = PolygonMetricLayer.filter(
        metric=metric_id,
        polygon=polygon,
        class_id=class_id,
        item_id=item_id,
        group_name=normalize_metric_group(metric_id, group),
    )
    if db is not None:
        query = query.using_db(db)
    return await query.first()


async def create_polygon_metric_layer(
    metric_obj: Metric,
    polygon_obj: Polygon,
    class_id: str,
    item_id: str,
    image_url: str,
    group: str | None = None,
    db: BaseDBAsyncClient | None = None,
):
    create_kwargs = {}
    if db is not None:
        create_kwargs["using_db"] = db
    try:
        await PolygonMetricLayer.create(
            metric=metric_obj,
            polygon=polygon_obj,
            class_id=class_id,
            item_id=item_id,
            group_name=normalize_metric_group(metric_obj, group),
            layer_url=image_url,
            **create_kwargs,
        )
    except IntegrityError as e:
        raise ServerError(
            code=500,
            usr_msg="There was an error saving the metric layer.",
            e=e,
        ) from e
