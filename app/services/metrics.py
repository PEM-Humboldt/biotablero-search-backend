from typing import List

import app.services.utils.raster as raster_utils
from app.routes.schemas.PolygonRequest import PolygonGeometry
from app.services.utils.collection import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.routes.schemas.MetricResponse import MetricResponse
from app.services.utils.metadata import fetch_collection_metadata
from app.services.utils.metrics_config import metric_group_key


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


def get_layer_by_defined_area(metric_id, area_type, area_id):
    # TODO: Implement service
    return ""


def get_layer_by_polygon(
    metric_id: str, polygon, item_id: str, category: int
) -> str:
    categories, values, colors = fetch_collection_metadata(metric_id)

    raster_href = get_asset_href_by_item_id(metric_id, item_id)

    cropped_raster = raster_utils.crop_raster(
        raster_href, polygon, category, values, colors
    )
    return cropped_raster
