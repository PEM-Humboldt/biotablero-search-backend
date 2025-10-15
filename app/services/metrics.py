from typing import List

import app.services.utils.raster as raster_utils
from app.persistence.polygon_metric_persistence import create_polygon_metric
from geojson_pydantic import geometries
from app.services.utils.collection import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.services.utils.metadata import fetch_collection_metadata
from fastapi import HTTPException
from app.models.models import Metric, Polygon, PolygonMetric
from app.utils.metrics_config import metric_group_key, build_metric_response
from app.utils.s3_utils import upload_to_s3
from app.routes.schemas.LayerResponse import LayerResponse
from app.persistence.layer_persistence import (
    get_existing_layer,
    save_layer_record,
)
from app.services.utils.raster import crop_raster


async def get_areas_by_polygon(
    metric_name: str, polygon: geometries.MultiPolygon
) -> List[dict]:
    categories, _, _, collection_name = await fetch_collection_metadata(
        metric_name
    )
    assets_url = get_items_asset_url(collection_name)
    result = []

    for k, v in assets_url.items():
        raster_values = raster_utils.get_raster_values(v, polygon, categories)
        response = {metric_group_key(metric_name): k}
        for class_name in categories.keys():
            response[class_name.lower()] = raster_values.get(class_name, 0)
        result.append(response)

    return result


async def get_or_create_polygon_metric(
    polygon_id: int, metric_name: str
) -> List[dict]:
    """
    Checks if metric values already exist for the given polygon and metric.
    If they exist, return them. Otherwise, calculate, persist, and return.
    """
    polygon_obj = await Polygon.get_or_none(id=polygon_id)
    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    metric_obj = await Metric.get_or_none(short_name=metric_name)

    if not metric_obj:
        raise HTTPException(
            status_code=400, detail="Metric not found in database"
        )

    metric = await PolygonMetric.get_or_none(
        polygon=polygon_obj, metric=metric_obj.id
    )

    if metric:
        return build_metric_response(metric_name, metric.values)

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    values = await get_areas_by_polygon(metric_name, polygon)
    await create_polygon_metric(polygon_obj, metric_obj, values)
    return build_metric_response(metric_name, values)


async def get_or_create_layer_by_polygon(
    metric_name: str, polygon_id: int, item_id: str, category: int
) -> LayerResponse:
    """
    Checks if the layer already exists. If not, generates it, saves and returns the URL.
    """
    metric_obj = await Metric.get_or_none(short_name=metric_name)

    if not metric_obj:
        raise HTTPException(
            status_code=400, detail="Metric not found in database"
        )

    polygon_obj = await Polygon.get_or_none(id=polygon_id)

    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    existing_item = await get_existing_layer(
        metric_obj.id, polygon_id, category, item_id
    )

    if existing_item:
        return LayerResponse(layer=existing_item.layer_url)

    _, values, colors, collection_name = await fetch_collection_metadata(
        metric_name
    )
    raster_href = get_asset_href_by_item_id(collection_name, item_id)

    image_base64 = crop_raster(
        raster_path=raster_href,
        polygon=polygon_obj.geometry,
        category=category,
        values=values,
        colors=colors,
    )

    image_url = await upload_to_s3(
        image_data=image_base64,
        filename=f"{metric_name}_{polygon_id}_{item_id}_{category}.png",
        content_type="image/png",
    )

    await save_layer_record(
        metric_obj=metric_obj,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        image_url=image_url,
    )

    return LayerResponse(layer=image_url)
