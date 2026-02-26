from app.models.models import Metric, PolygonMetricLayer, Polygon


async def get_existing_layer(
    metric_id: Metric, polygon: Polygon, class_id: str, item_id: str
):
    return await PolygonMetricLayer.get_or_none(
        metric=metric_id, polygon=polygon, class_id=class_id, item_id=item_id
    )


async def create_polygon_metric_layer(
    metric_obj: Metric,
    polygon_obj: Polygon,
    class_id: str,
    item_id: str,
    image_url: str,
):
    await PolygonMetricLayer.create(
        metric=metric_obj,
        polygon=polygon_obj,
        class_id=class_id,
        item_id=item_id,
        layer_url=image_url,
    )
