import app.services.utils.raster as raster_utils
from app.services.utils.collection import get_first_item_asset_from_collection
from app.utils import config
from app.routes.schemas.polygon import PolygonGeometry


settings = config.get_settings()


class Metrics:

    def get_areas_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_areas_by_polygon(
        polygon: PolygonGeometry, metric_id: str
    ) -> list[dict[str, float]]:

        first_asset = get_first_item_asset_from_collection(
            settings.stac_url, metric_id
        )
        raster_cloud_path = first_asset

        out_data = raster_utils.get_raster_values(raster_cloud_path, polygon)

        return out_data

    def get_layer_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_layer_by_polygon(metric_id: str, polygon: PolygonGeometry):

        first_asset = get_first_item_asset_from_collection(
            settings.stac_url, metric_id
        )

        raster_cloud_path = first_asset
        out_image = raster_utils.crop_raster(raster_cloud_path, polygon)
        return out_image
