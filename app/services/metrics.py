from typing import List

import app.services.utils.raster as raster_utils
from app.services.utils.collection import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.routes.schemas.polygon import PolygonGeometry
from app.routes.schemas.MetricValues import MetricResponse
from app.services.utils.metrics_config import (
    value_category_config,
    metric_group_key,
)


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

    assets_url = get_items_asset_url(metric_id)
    result = []
    for k, v in assets_url.items():
        values = raster_utils.get_raster_values(
            v, polygon, value_category_config(metric_id)
        )
        group = metric_group_key(metric_id)
        if group is None:
            # TODO: Change Exception for specific class
            raise Exception("there is not a defined category for this metric")
        values[group] = k
        result.append(values)

    return result


def get_layer_by_defined_area(metric_id, area_type, area_id):
    # TODO: Implement service
    return ""


def get_layer_by_polygon(
    metric_id: str, polygon: PolygonGeometry, item_id: str
):

    # TODO: change this line when the optimization strategy is implemented
    raster_href = get_asset_href_by_item_id(metric_id, item_id)

    out_image = raster_utils.crop_raster(raster_href, polygon)
    return out_image
