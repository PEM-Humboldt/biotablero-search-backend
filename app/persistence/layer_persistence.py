from app.models.models import Polygon, PolygonMetricItem


async def get_existing_layer(
    metric: str, polygon_id: int, category: int, item_id: str
):
    return await PolygonMetricItem.get_or_none(
        metric=metric,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
    )


async def save_layer_record(
    metric: str, polygon_id: int, category: int, item_id: str, image_url: str
):
    await PolygonMetricItem.create(
        metric=metric,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        layer_url=image_url,
    )
