import base64
import io

from PIL import Image
import numpy as np
from typing import Dict, List, Tuple, cast
from shapely import box
from shapely.ops import transform as shapely_transform
from shapely.geometry import shape, MultiPolygon, Polygon as ShapelyPolygon

import rasterio
from rasterio.crs import CRS
from rasterio.mask import mask
from rasterio.windows import from_bounds
from rasterio.features import rasterize
import gc

from pyproj import Transformer
from geojson_pydantic import geometries

from app.middleware.log_middleware import logger
from app.utils.errors import (
    NotFoundError,
    ServerError,
    UnprocessableError,
    MetadataError,
)


def crop_raster_by_polygon(
    raster_path: str,
    polygon: geometries.MultiPolygon,
) -> Tuple[np.ndarray, np.ndarray]:
    polygon_geom = shape(polygon)
    with rasterio.open(raster_path) as src:

        minx, miny, maxx, maxy = polygon_geom.bounds
        window = from_bounds(minx, miny, maxx, maxy, src.transform)
        data = src.read(1, window=window)
        data = np.where(np.isnan(data), 0, data)
        window_transform = src.window_transform(window)

        polygon_mask = rasterize(
            [polygon],
            out_shape=data.shape,
            transform=window_transform,
            fill=False,
            default_value=1,
            dtype=np.uint8,
        )

        masked_data = np.where(polygon_mask, data, np.nan)
        del data, polygon_mask
        gc.collect()
    return masked_data, window_transform


def get_one_raster_image(
    raster_path: str,
    polygon: geometries.MultiPolygon,
    class_value: int,
    values: List[int],
    colors: List[str],
) -> str:
    Image.MAX_IMAGE_PIXELS = None

    colormap: Dict[int, Tuple[int, int, int, int]] = {
        value: hex_to_rgba(color) for value, color in zip(values, colors)
    }
    if class_value not in colormap:
        raise MetadataError(
            code=501,
            usr_msg="There was an internal error processing the request",
            log_msg=f"Class {class_value} not found in the colors metadata.",
        )

    masked_data, _ = crop_raster_by_polygon(raster_path, polygon)
    if len(masked_data) == 0 or np.all(masked_data != class_value):
        raise NotFoundError(
            usr_msg="No data available for the selected class.",
            log_msg=f"No data generated for class value {class_value}.",
        )
    try:
        h, w = masked_data.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)

        rgba[masked_data == class_value] = colormap[class_value]

        pil_image = Image.fromarray(rgba, mode="RGBA")
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        del masked_data, rgba, img_buffer, pil_image
    except Exception as e:
        logger.error(
            f"Unexpected error rendering class value {class_value}: {str(e)}"
        )
        raise ServerError(
            code=500,
            usr_msg=f"There was an error processing the requested class.",
            e=e,
        )
    gc.collect()
    return img_base64


def get_one_raster_areas(
    raster_path: str,
    polygon: geometries.MultiPolygon,
    categories: Dict[str, int],
) -> Dict[str, float]:
    """
    Calculate areas for every category from the raster in a given polygon.
    """
    polygon_geom = shape(polygon)

    source_crs = CRS.from_string("EPSG:4326")

    with rasterio.open(raster_path) as src:
        raster_bounds = box(*src.bounds)
        if not polygon_geom.intersects(raster_bounds):
            raise UnprocessableError(
                code=422,
                usr_msg="Input polygon does not intersect with metric.",
                e=Exception("Polygon does not intersect with raster bounds"),
            )

        if isinstance(polygon_geom, MultiPolygon):
            multi_poly = cast(MultiPolygon, polygon_geom)
            polygon_geoms = list(multi_poly.geoms)
        elif isinstance(polygon_geom, ShapelyPolygon):
            polygon_geoms = [polygon_geom]
        else:
            polygon_geoms = [polygon_geom]

        if src.crs != source_crs:
            transformer = Transformer.from_crs(
                source_crs, src.crs, always_xy=True
            )
            reprojected_geoms = []
            for geom in polygon_geoms:
                if isinstance(geom, ShapelyPolygon):
                    poly = cast(ShapelyPolygon, geom)
                    polygon_coords = list(poly.exterior.coords)
                    transformed_coords = [
                        transformer.transform(x, y) for x, y in polygon_coords
                    ]
                    reprojected_geoms.append(
                        ShapelyPolygon(transformed_coords)
                    )
                else:
                    reprojected_geoms.append(
                        shapely_transform(transformer.transform, geom)
                    )
            polygon_geoms = reprojected_geoms

        raster_data, raster_transform = mask(
            src,
            polygon_geoms,
            crop=True,
            nodata=src.nodata if src.nodata is not None else -9999,
        )
        raster_data = raster_data[0]
        raster_nodata = src.nodata if src.nodata is not None else -9999

        pixel_size_x = abs(raster_transform[0])
        pixel_size_y = abs(raster_transform[4])

        transformer = Transformer.from_crs(
            "EPSG:4326", "EPSG:9377", always_xy=True
        )

        center_x = raster_transform[2]
        center_y = raster_transform[5]

        corners_geo = [
            (center_x, center_y),
            (center_x + pixel_size_x, center_y),
            (center_x + pixel_size_x, center_y + pixel_size_y),
            (center_x, center_y + pixel_size_y),
        ]

        corners_projected = [
            transformer.transform(x, y) for x, y in corners_geo
        ]

        pixel_polygon = ShapelyPolygon(corners_projected)
        pixel_area_m2 = pixel_polygon.area

        pixel_area_ha = float(pixel_area_m2 / 10000)

        if raster_nodata is not None:
            valid_mask = raster_data != raster_nodata
        else:
            valid_mask = np.ones_like(raster_data, dtype=bool)

        if np.issubdtype(raster_data.dtype, np.floating):
            valid_mask = valid_mask & ~np.isnan(raster_data)

        valid_data = raster_data[valid_mask]

        unique_values, counts = np.unique(valid_data, return_counts=True)

        value_to_category = {val: name for name, val in categories.items()}

        areas_by_category = {
            category_key: 0.0 for category_key in categories.keys()
        }

        for value, pixel_count in zip(unique_values, counts):
            area_ha = float(pixel_count * pixel_area_ha)

            if value in value_to_category:
                category_key = value_to_category[value]
                areas_by_category[category_key] = area_ha
            else:
                areas_by_category[str(int(value))] = area_ha

        return areas_by_category


def get_one_raster_average(
    raster_path: str,
    polygon: geometries.MultiPolygon,
) -> float:
    """
    Calculate average in a given polygon.
    """
    polygon_geom = shape(polygon)

    source_crs = CRS.from_string("EPSG:4326")

    with rasterio.open(raster_path) as src:
        raster_bounds = box(*src.bounds)
        if not polygon_geom.intersects(raster_bounds):
            raise UnprocessableError(
                code=422,
                usr_msg="Input polygon does not intersect with metric.",
                e=Exception("Polygon does not intersect with raster bounds"),
            )

        if src.crs != source_crs:
            transformer = Transformer.from_crs(
                source_crs, src.crs, always_xy=True
            )
            polygon_geom = shapely_transform(
                transformer.transform, polygon_geom
            )

        raster_data, _ = mask(
            src,
            [polygon_geom],
            crop=True,
            nodata=src.nodata if src.nodata is not None else -9999,
        )
        raster_data = raster_data[0]
        raster_nodata = src.nodata if src.nodata is not None else -9999
        valid_data = raster_data[raster_data != raster_nodata]

        average_value = float(np.nanmean(valid_data))

        return average_value


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    if hex_color.startswith("#"):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            return r, g, b, 255
        else:
            raise ValueError(f"Invalid hex color format: {hex_color}")
    raise ValueError(f"Hex color must start with '#': {hex_color}")
