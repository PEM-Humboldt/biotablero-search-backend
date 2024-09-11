import subprocess

import numpy as np
import rasterio
import rasterstats
from geopandas import GeoDataFrame
from rasterio._warp import Resampling
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform, reproject
from rio_tiler.io.rasterio import Reader
from rasterstats import zonal_stats
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import shape as shapely_shape, shape, box
import pandas as pd
from typing import Dict, Any, List
import matplotlib.pyplot as plt
from pyproj import Transformer
from shapely.ops import transform
from pyproj import Transformer
from shapely.ops import transform
from shapely.geometry import shape
from typing import Dict, Any
from rasterstats import zonal_stats
import rasterio
from rasterio.crs import CRS
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


# TODO: Test the data resulting from the areas

def crop_raster_to_polygon(src, polygon_gdf):
    """
    Recorta el raster al área del polígono.
    """
    from rasterio.features import geometry_mask

    # Obtener la máscara del polígono
    out_image, out_transform = mask(src, polygon_gdf.geometry, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "count": 1,
                     "width": out_image.shape[2],
                     "height": out_image.shape[1],
                     "transform": out_transform})

    return out_image, out_meta

def reproject_raster_in_memory(meta, raster, dst_crs):
    """
    Reproyecta un raster en memoria.
    """
    src_crs = meta['crs']
    src_transform = meta['transform']
    src_width = meta['width']
    src_height = meta['height']

    # Calcular los límites del raster
    src_bounds = (
        src_transform.c,
        src_transform.f + src_height * src_transform.e,
        src_transform.c + src_width * src_transform.a,
        src_transform.f
    )

    # Calcular la nueva transformación y el tamaño del raster reproyectado
    transform, width, height = calculate_default_transform(
        src_crs,
        dst_crs,
        src_width,
        src_height,
        *src_bounds
    )

    # Preparar un nuevo array para el raster reproyectado
    reprojected_raster = np.empty((raster.shape[0], height, width), dtype=raster.dtype)

    # Realizar la reproyección
    reproject(
        source=raster,
        destination=reprojected_raster,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )

    # Actualizar los metadatos del raster reproyectado
    new_meta = meta.copy()
    new_meta.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    return reprojected_raster, new_meta

def get_raster_values(raster_path: str, polygon: PolygonGeometry, categories: Dict[str, int]) -> Dict[str, Any]:
    """
    Recorta el raster al polígono, lo reproyecta y realiza análisis zonal por categorías.
    """
    # Convertir el PolygonGeometry en un GeoDataFrame
    polygon_shape = shape(polygon)  # Asegurarse de que el polígono esté en formato shapely
    polygon_gdf = gpd.GeoDataFrame(geometry=[polygon_shape], crs="EPSG:4326")  # Asumir que el CRS original es EPSG:4326

    # Leer el archivo raster original
    with rasterio.open(raster_path) as src:
        # Recortar el raster al área del polígono
        cropped_raster, cropped_meta = crop_raster_to_polygon(src, polygon_gdf)

        # Reproyectar solo el raster recortado en memoria
        reprojected_raster, reprojected_meta = reproject_raster_in_memory(cropped_meta, cropped_raster, dst_crs="EPSG:9377")

        # Convertir el polígono al CRS del raster reproyectado
        polygon_reprojected = polygon_gdf.to_crs(epsg=9377)

        # Realizar el análisis zonal utilizando RasterStats
        stats = zonal_stats(
            polygon_reprojected,
            reprojected_raster[0],  # Utilizar el primer canal del raster
            affine=reprojected_meta['transform'],
            stats="sum",  # Puedes ajustar a los cálculos que necesites
            nodata=-999,
            categorical=True  # Hacer el análisis por categorías
        )

        # Verificar que stats sea una lista de diccionarios
        if not isinstance(stats, list) or not isinstance(stats[0], dict):
            raise ValueError("Error en el resultado de zonal_stats, no contiene datos válidos.")

        # Crear un diccionario con las áreas calculadas por categoría
        areas = stats[0]  # stats[0] es un diccionario con las categorías y sus valores

        # Mapeo de las categorías específicas
        output_data = {key: areas.get(categories[key], 0) for key in categories}

        return output_data