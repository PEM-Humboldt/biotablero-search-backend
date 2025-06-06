from typing import List

import app.services.utils.raster as raster_utils
from app.persistence.polygon_metric_persistence import create_polygon_metric
from app.routes.schemas.PolygonRequest import PolygonGeometry
from app.services.utils.collection import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.routes.schemas.MetricResponse import MetricResponse
from app.services.utils.metadata import fetch_collection_metadata
from app.services.utils.metrics_config import metric_group_key
from fastapi import HTTPException
from app.models.models import Polygon, PolygonMetric
from app.utils.s3_utils import upload_to_s3
from app.routes.schemas.MetricResponse import LayerResponse
from app.persistence.layer_persistence import (
    get_existing_layer,
    save_layer_record,
)
from app.services.utils.raster import crop_raster


def get_areas_by_polygon(
    metric_id: str, polygon: PolygonGeometry
) -> List[MetricResponse]:

    categories, _, _ = fetch_collection_metadata(metric_id)

    assets_url = get_items_asset_url(metric_id)

    result = []

    for k, v in assets_url.items():
        raster_values = raster_utils.get_raster_values(v, polygon, categories)

        response = {metric_group_key(metric_id): k}

        for class_name in categories.keys():
            response[class_name] = raster_values.get(class_name, 0)

        result.append(response)

    return result


async def get_or_create_polygon_metric(
    polygon_id: int, metric_id: str
) -> list:
    """
    Checks if metric values already exist for the given id.
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

    polygon = PolygonGeometry(**polygon_obj.geometry)

    values = get_areas_by_polygon(metric_id, polygon)

    await create_polygon_metric(polygon_obj, metric_id, values)
    return values


async def get_or_create_layer_by_polygon(
    metric_id: str, polygon_id: int, item_id: str, category: int
) -> LayerResponse:    
    """
    Checks if the layer already exists for the specified parameters.
    If it exists, it is returned. Otherwise, it is calculated, retained, and the result is returned.
    """

    polygon_obj = await Polygon.get_or_none(id=polygon_id)
    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    existing_item = await get_existing_layer(
        metric_id, polygon_id, category, item_id
    )
    if existing_item:
        return LayerResponse(layer=existing_item.layer_url)

    _, values, colors = fetch_collection_metadata(metric_id)

    raster_href = get_asset_href_by_item_id(metric_id, item_id)

    image_base64 = crop_raster(
        raster_path=raster_href,
        polygon=polygon_obj.geometry,
        category=category,
        values=values,
        colors=colors,
    )

    image_url = await upload_to_s3(
        image_data=image_base64,
        filename=f"{metric_id}_{polygon_id}_{item_id}_{category}.png",
        content_type="image/png",
    )

    await save_layer_record(
        metric=metric_id,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        image_url=image_url,
    )

    return LayerResponse(layer=image_url)
