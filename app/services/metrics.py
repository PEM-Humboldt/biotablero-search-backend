from typing import List, Dict

import app.services.utils.raster as raster_utils
from app.services.utils.collection import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.routes.schemas.polygon import PolygonGeometry
from app.routes.schemas.MetricValues import MetricResponse
from app.services.utils.metadata import fetch_collection_metadata
from app.services.utils.metrics_config import metric_group_key


def get_areas_by_defined_area(
    metric_id, area_type, area_id
) -> List[MetricResponse]:
    # TODO: Implement service
    return [
        {
            "perdida": 2035,
            "persistencia": 40843,
            "no_bosque": 207122,
            "periodo": "dummy",
        }
    ]


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
) -> Dict[str, str]:
    categories, values, colors = fetch_collection_metadata(metric_id)

    raster_href = get_asset_href_by_item_id(metric_id, item_id)

    base64_images = raster_utils.crop_raster(
        raster_href, polygon, category, values, colors
    )
    return base64_images
