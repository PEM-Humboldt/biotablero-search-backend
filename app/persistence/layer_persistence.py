from app.models.models import Metric, PolygonMetricItem


async def get_existing_layer(
    metric_id: int, polygon_id: int, category: int, item_id: str
):
    return await PolygonMetricItem.get_or_none(
        metric=metric_id,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
    )


async def save_layer_record(
    metric_obj: Metric,
    polygon_id: int,
    category: int,
    item_id: str,
    image_url: str,
):
    await PolygonMetricItem.create(
        metric=metric_obj,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        layer_url=image_url,
    )
