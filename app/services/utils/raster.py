from rio_tiler.io import Reader
from rasterio import features
from geopandas import GeoDataFrame
from shapely import geometry


# TODO: become generic in order to be able to reuse
def crop_raster(raster_path, polygon):
    with Reader(raster_path) as image:
        img = image.feature(polygon)

    return img.render(
        add_mask=True,
        colormap={
            0: (255, 0, 0, 255),
            1: (128, 204, 102, 255),
            2: (232, 214, 107, 255),
        },
    )


def get_raster_values(raster_path, polygon):
    crs = "EPSG:9377"
    categories = {"Perdida": 0, "Persistencia": 1, "No bosque": 2}

    with Reader(raster_path) as cog:
        data = cog.feature(polygon, dst_crs=crs)
        transform = data.transform
        mask = data.mask != 0

        data_shapes = features.shapes(
            data.data[0], mask=mask, transform=transform
        )

        geometries = []
        values = []
        for geom, value in data_shapes:
            geometries.append(geometry.shape(geom))
            values.append(value)

        dataFrame = GeoDataFrame({"value": values, "geometry": geometries})

        dataFrame["area"] = dataFrame.geometry.area

        areas = dataFrame.groupby("value")["area"].sum() / 10000

        output_data = [
            {"key": key, "value": areas[categories[key]]} for key in categories
        ]

        return output_data
