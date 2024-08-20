from rio_tiler.io.rasterio import Reader
from rasterio import features
from geopandas import GeoDataFrame
from shapely import geometry
from typing import Any


# TODO: become generic in order to be able to reuse
def crop_raster(raster_path, polygon):
    with Reader(input= raster_path, options={}) as image:
        img = image.feature(polygon)

    return img.render(
        add_mask=True,
        colormap={
            0: (255, 0, 0, 255),
            1: (128, 204, 102, 255),
            2: (232, 214, 107, 255),
        },
    )


# TODO: Test the data resulting from the areas
def get_raster_values(raster_path, polygon, categories) -> dict[str, Any]:
    crs = "EPSG:9377"

    with Reader(input=raster_path, options={}) as cog:
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

        output_data = {key: areas[categories[key]] for key in categories}

        return output_data
