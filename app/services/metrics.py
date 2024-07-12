import app.services.utils.raster as raster_utils

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


class Metrics:

    def get_areas_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_areas_by_polygon(polygon):
        # TODO: read raster from STAC
        raster_cloud_path = "https://staccatalog.blob.core.windows.net/cog-test/Colombia_pp-2015_12_31-pp_2011_2015.tif"
        out_data = raster_utils.get_raster_values(raster_cloud_path, polygon)
        return out_data

    def get_layer_by_defined_area(area_type, area_id):
        # TODO: Implement service
        return ""

    def get_layer_by_polygon(metric_id, polygon):

        collection_metric = next(
            (
                collection
                for collection in collections
                if collection["id"] == metric_id
            ),
            None,
        )

        # TODO: Handle error when colection in no defined or the cog attribute does not exist
        if collection_metric and "cog" in collection_metric:
            cog_url = collection_metric["cog"]

        out_image = raster_utils.crop_raster(cog_url, polygon)
        return out_image
