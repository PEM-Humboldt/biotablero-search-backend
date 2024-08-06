from typing import Dict, Any

import app.services.utils.raster as raster_utils
from app.services.read_coleccion import find_collection_url, get_collection_items_url, load_first_item_asset
from app.utils import config
from app.routes.schemas.polygon import PolygonFeature, PolygonGeometry



settings = config.get_settings()


class Metrics:

    def get_areas_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_areas_by_polygon(polygon: PolygonGeometry, metric_id: str) -> dict[str, Any]:
        collection_url = find_collection_url(settings.stac_url, metric_id)

        if not collection_url:
            raise ValueError(f"No collection found for id: {metric_id}")

        items_url = get_collection_items_url(collection_url)

        if not items_url:
            raise ValueError(f"No items URL found for collection id: {metric_id}")

        first_asset = load_first_item_asset(items_url)

        if not first_asset:
            raise ValueError(f"No valid asset found for metric id: {metric_id}")

        raster_cloud_path = first_asset['href']

        out_data = raster_utils.get_raster_values(raster_cloud_path, polygon)

        return out_data

    def get_layer_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_layer_by_polygon(metric_id: str, polygon: PolygonGeometry):
        collection_url = find_collection_url(settings.stac_url, metric_id)

        if not collection_url:
            raise ValueError(f"No collection found for id: {metric_id}")

        items_url = get_collection_items_url(collection_url)

        if not items_url:
            raise ValueError(f"No items URL found for collection id: {metric_id}")

        first_asset = load_first_item_asset(items_url)

        if not first_asset:
            raise ValueError(f"No valid asset found for metric id: {metric_id}")

        raster_cloud_path = first_asset['href']
        out_image = raster_utils.crop_raster(raster_cloud_path, polygon)
        return out_image
