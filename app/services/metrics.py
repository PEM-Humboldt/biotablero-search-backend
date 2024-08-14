import app.services.utils.raster as raster_utils
from app.services.utils.collection import get_items_asset_url
from app.routes.schemas.polygon import PolygonGeometry
from app.services.utils.metrics_config import (
    value_category_config,
    metric_group_key,
)


class Metrics:

    def get_areas_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_areas_by_polygon(
        metric_id: str, polygon: PolygonGeometry
    ) -> list[dict[str, float]]:

        assets_url = get_items_asset_url(metric_id)
        result = []
        for k, v in assets_url.items():
            values = raster_utils.get_raster_values(
                v, polygon, value_category_config(metric_id)
            )
            values[metric_group_key(metric_id)] = k
            result.append(values)

        return result

    def get_layer_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_layer_by_polygon(metric_id: str, polygon: PolygonGeometry):

        # TODO: change this line when the optimization strategy is implemented
        first_asset = get_items_asset_url(metric_id)[0]

        out_image = raster_utils.crop_raster(
            first_asset, polygon, value_category_config(metric_id)
        )
        return out_image
