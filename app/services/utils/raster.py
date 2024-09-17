import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

import pandas as pd
import pyproj
import rasterio
import shapely
from geopandas import GeoDataFrame

from pyproj import Transformer, CRS
from rasterio import features
from rasterio.enums import Resampling
from rasterio.features import shapes as rasterio_shapes, shapes
from rasterio.warp import calculate_default_transform, reproject
from rasterio.windows import from_bounds
from rasterstats import zonal_stats
from rio_tiler.io import COGReader
from rasterio import open as rio_open
from rio_tiler.io.rasterio import Reader
import numpy as np
from rasterio.mask import mask
import geopandas as gpd
from typing import Any, Dict
from fiona.transform import transform_geom
from rioxarray import rioxarray
from shapely import transform, Polygon, geometry
from shapely.geometry import shape, polygon

from app.middleware.log_middleware import logger

from app.routes.schemas.polygon import PolygonGeometry


# TODO: become generic in order to be able to reuse
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


def get_raster_values(raster_path: str, polygon: geometry.Polygon, categories: Dict[str, int]) -> Dict[str, Any]:
    start_time = time.time()

    # Crear un GeoDataFrame del polígono y obtener su CRS
    gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="EPSG:4326")  # Suponiendo que el polígono está en EPSG:4326
    target_crs = "EPSG:9377"  # CRS de destino

    # Cargar el raster con rioxarray
    raster_open_start = time.time()
    raster = rioxarray.open_rasterio(raster_path, masked=True)
    raster_open_end = time.time()
    print(f"Time to open raster: {raster_open_end - raster_open_start:.2f} seconds")

    # Obtener y mostrar el CRS del raster
    raster_crs = raster.rio.crs
    print(f"CRS in rioxarray: {raster_crs}")

    # Recortar el raster usando el polígono (sin reproyectar aún)
    clip_start = time.time()
    clipped_raster = raster.rio.clip(gdf.geometry, from_disk=True)
    clip_end = time.time()
    print(f"Time to clip raster: {clip_end - clip_start:.2f} seconds")

    # Reproyectar el raster recortado al CRS de destino
    reproject_raster_start = time.time()
    if clipped_raster.rio.crs != target_crs:
        clipped_raster = clipped_raster.rio.reproject(target_crs)
    reproject_raster_end = time.time()
    print(f"Time to reproject clipped raster: {reproject_raster_end - reproject_raster_start:.2f} seconds")

    # Obtener y mostrar la matriz de transformación del raster reproyectado
    reprojected_transform = clipped_raster.rio.transform()
    reprojected_transform_matrix = np.array(reprojected_transform).reshape(3, 3)
    print(f"Transformation matrix after reprojection:\n{reprojected_transform_matrix}")

    # Ahora reproyectar el polígono al mismo CRS que el raster
    if gdf.crs != target_crs:
        print("Reprojecting polygon to match raster CRS...")
        gdf = gdf.to_crs(target_crs)

    # Usar zonal_stats para calcular áreas por categoría
    calc_stats_start = time.time()
    stats = zonal_stats(
        gdf,
        clipped_raster.values[0],  # Usar la primera banda del raster
        affine=clipped_raster.rio.transform(),
        categorical=True,  # Para obtener el área por categoría
        nodata=np.nan  # Definir los valores nulos
    )
    calc_stats_end = time.time()
    print(f"Time to calculate zonal stats: {calc_stats_end - calc_stats_start:.2f} seconds")

    # Extraer las áreas por categoría desde los resultados
    areas_by_category = stats[0]  # Solo hay una geometría, por eso tomamos el primer elemento de la lista

    # Convertir las áreas de píxeles a hectáreas (asumiendo 1 píxel = 1m²)
    pixel_area_m2 = abs(clipped_raster.rio.transform()[0]) ** 2  # Calcular el área en m² de un píxel
    pixel_area_ha = pixel_area_m2 / 10000  # Convertir el área a hectáreas

    # Preparar el diccionario de resultados con las áreas por categoría
    output_data = {}
    for category, pixel_count in areas_by_category.items():
        area_ha = pixel_count * pixel_area_ha  # Convertir el conteo de píxeles a hectáreas
        if category in categories.values():
            category_key = [key for key, val in categories.items() if val == category][0]
            output_data[category_key] = area_ha

    end_time = time.time()
    print(f"Total Execution Time: {end_time - start_time:.2f} seconds")

    return output_data
