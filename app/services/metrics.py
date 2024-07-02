import app.utils.raster as raster_utils


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

    def get_layer_by_polygon(polygon):
        # TODO: read raster from STAC
        raster_cloud_path = "https://staccatalog.blob.core.windows.net/cog-test/Colombia_pp-2015_12_31-pp_2011_2015.tif"

        out_image = raster_utils.crop_raster(raster_cloud_path, polygon)
        return out_image
