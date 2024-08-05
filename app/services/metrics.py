from typing import Dict, Any

import app.services.utils.raster as raster_utils
from app.services.read_coleccion import load_collection_items
from app.utils import config
from app.routes.schemas.polygon import PolygonFeature, PolygonGeometry

# TODO: Read the collections list from STAC. Id collection should be match to metric id
collections = [
    {
        "id": "LossPersistence",
        "cog": "https://staccatalog.blob.core.windows.net/cog-test/Colombia_pp-2015_12_31-pp_2011_2015.tif",
    },
    {
        "id": "Coverage",
        "cog": "https://coverage-example.tif",
    },
]

settings = config.get_settings()


class Metrics:

    def get_areas_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_areas_by_polygon(polygon: PolygonGeometry, collection_id: str) -> dict[str, Any]:
        items = load_collection_items(f"{settings.stac_url}", collection_id)

        if not items:
            raise ValueError(f"No items found for collection id: {collection_id}")

        first_item = items[0]

        if not first_item:
            raise ValueError(f"No valid item found for collection id: {collection_id}")

        raster_cloud_path = f"{settings.cog_base_url}/{first_item['assets']['input_file']}"

        out_data = raster_utils.get_raster_values(raster_cloud_path, polygon)

        return out_data

    def get_layer_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_layer_by_polygon(metric_id: str, polygon_feature: PolygonFeature):
        items = load_collection_items(f"{settings.stac_url}", metric_id)

        if not items:
            raise ValueError(f"No items found for collection id: {metric_id}")

        first_item = items[0]

        if not first_item:
            raise ValueError(f"No valid item found for metric id: {metric_id}")

        raster_cloud_path = f"{config.Settings.COG_BASE_URL}/{first_item['assets']['input_file']}"
        out_data = raster_utils.get_raster_values(raster_cloud_path, polygon_feature)
        return out_data
