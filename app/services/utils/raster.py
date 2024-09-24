from rasterstats import zonal_stats
from rio_tiler.io.rasterio import Reader
import numpy as np
import geopandas as gpd
from typing import Any, Dict
import rioxarray
from shapely import geometry


# TODO: define how to get the color map (db, object, etc), it can't be hardcoded here
def crop_raster(raster_path, polygon):
    with Reader(input=raster_path, options={}) as image:
        img = image.feature(polygon)

    return img.render(
        add_mask=True,
        colormap={
            0: (255, 0, 0, 255),
            1: (128, 204, 102, 255),
            2: (232, 214, 107, 255),
        },
    )


# TODO: verify if categories should be kept as object or if it should be get from the db
def get_raster_values(
    raster_path: str, polygon: geometry.Polygon, categories: Dict[str, int]
) -> Dict[str, Any]:
    gdf = gpd.GeoDataFrame(
        {"geometry": [polygon]}, crs="EPSG:4326"
    )  # type: ignore -> https://github.com/geopandas/geopandas/issues/3115
    target_crs = "EPSG:9377"

    raster = rioxarray.open_rasterio(raster_path, masked=True)

    clipped_raster = raster.rio.clip(gdf.geometry, from_disk=True)

    if clipped_raster.rio.crs != target_crs:
        clipped_raster = clipped_raster.rio.reproject(target_crs)

    if gdf.crs != target_crs:
        gdf = gdf.to_crs(target_crs)

    stats = zonal_stats(
        gdf,
        clipped_raster.values[0],  # Usar la primera banda del raster
        affine=clipped_raster.rio.transform(),
        categorical=True,  # Para obtener el área por categoría
        nodata=np.nan,  # Definir los valores nulos
    )

    areas_by_category = stats[0]

    pixel_area_m2 = abs(clipped_raster.rio.transform()[0]) ** 2
    pixel_area_ha = pixel_area_m2 / 10000

    output_data = {}
    for category, pixel_count in areas_by_category.items():
        area_ha = pixel_count * pixel_area_ha
        if category in categories.values():
            category_key = [
                key for key, val in categories.items() if val == category
            ][0]
            output_data[category_key] = area_ha

    return output_data
