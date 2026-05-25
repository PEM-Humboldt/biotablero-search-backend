import base64
import io

from PIL import Image
import numpy as np
from typing import Dict, List, Optional, Tuple
from shapely import box
from shapely.ops import transform as shapely_transform
from shapely.geometry import shape, Polygon as ShapelyPolygon, MultiPolygon

import rasterio
from rasterio.crs import CRS
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


def _crop_raster_by_polygon(
    raster_path: str,
    polygon: geometries.MultiPolygon,
) -> Tuple[np.ndarray, np.ndarray, Optional[float]]:
    """Crop a raster by a given polygon and return the masked data, the window transform, and the nodata value."""

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

        minx, miny, maxx, maxy = polygon_geom.bounds
        window = from_bounds(minx, miny, maxx, maxy, src.transform)
        window_transform = src.window_transform(window)
        data = src.read(1, window=window)
        if data is None:
            raise ValueError("Could not read raster data")
        data = data.astype(np.float64)

        src_nodata = src.nodata

        polygon_mask = rasterize(
            [polygon_geom],
            out_shape=data.shape,
            transform=window_transform,
            fill=False,
            default_value=True,
            dtype=np.uint8,
        )
        if polygon_mask is None:
            raise ValueError("Failed to rasterize polygon")

        masked_data = np.where(polygon_mask.astype(bool), data, np.nan)
        del data, polygon_mask
        gc.collect()
    return masked_data, window_transform, src_nodata


def _get_raster_pixel_area_ha(raster_transform, raster_crs) -> float:
    """
    Calculate the area in hectares of a pixel given a raster transform and CRS.
    """
    pixel_size_x = abs(raster_transform[0])
    pixel_size_y = abs(raster_transform[4])

    center_x = raster_transform[2]
    center_y = raster_transform[5]

    corners_geo = [
        (center_x, center_y),
        (center_x + pixel_size_x, center_y),
        (center_x + pixel_size_x, center_y + pixel_size_y),
        (center_x, center_y + pixel_size_y),
    ]

    transformer = Transformer.from_crs(raster_crs, "EPSG:9377", always_xy=True)
    corners_projected = [transformer.transform(x, y) for x, y in corners_geo]

    pixel_polygon = ShapelyPolygon(corners_projected)
    return float(pixel_polygon.area / 10_000)


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

    masked_data, _, _ = _crop_raster_by_polygon(raster_path, polygon)

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


def get_one_raster_areas_by_classes(
    raster_path: str,
    polygon: geometries.MultiPolygon,
    classes: Dict[str, int],
) -> Dict[str, float]:
    """
    Calculate areas for every category from the raster in a given polygon.
    """

    masked_data, raster_transform, _ = _crop_raster_by_polygon(
        raster_path, polygon
    )

    pixel_area_ha = _get_raster_pixel_area_ha(raster_transform, "EPSG:4326")
    clean_data = masked_data[~np.isnan(masked_data)].astype(int)

    value_to_class = {val: name for name, val in classes.items()}
    unique_values, counts = np.unique(clean_data, return_counts=True)

    areas_by_class = {class_key: 0.0 for class_key in classes.keys()}

    for value, pixel_count in zip(unique_values, counts):
        area_ha = float(pixel_count * pixel_area_ha)

        if value in value_to_class:
            class_key = value_to_class[value]
            areas_by_class[class_key] = area_ha
        else:
            areas_by_class[str(int(value))] = area_ha

    return areas_by_class


def get_two_raster_areas_by_classes(
    raster1_path: str,
    raster2_path: str,
    polygon: geometries.MultiPolygon,
    classes: Dict[str, int],
) -> Dict[str, float]:
    """
    Calculates the area (in ha) by class of a raster within a polygon,
    but only where it intersects a second raster.
    """
    # TODO: optimizarla usando la función _crop_raster_by_polygon

    polygon_geom = shape(polygon)

    value_to_class = {val: name for name, val in classes.items()}
    areas_by_class = {class_key: 0.0 for class_key in classes.keys()}
    with rasterio.open(raster1_path) as src:
        raster_bounds = box(*src.bounds)
        if not polygon_geom.intersects(raster_bounds):
            raise UnprocessableError(
                code=422,
                usr_msg="Input polygon does not intersect with metric.",
                e=Exception("Polygon does not intersect with raster bounds"),
            )

        with rasterio.open(raster2_path) as mask_src:
            if src.crs != mask_src.crs:
                raise ValueError(
                    "Raster coordinate reference systems do not match."
                )
            if src.res != mask_src.res:
                raise ValueError("Raster resolutions do not match.")

            minx, miny, maxx, maxy = polygon_geom.bounds
            window = from_bounds(minx, miny, maxx, maxy, src.transform)
            window_mask = from_bounds(
                minx, miny, maxx, maxy, mask_src.transform
            )
            src_nanvalue = src.nodata
            mask_src_nanvalue = mask_src.nodata

            data = src.read(1, window=window)
            mask_data = mask_src.read(1, window=window_mask)

            if src_nanvalue is None:
                pass
            elif np.isnan(src_nanvalue):
                data = np.where(np.isnan(data), 0, data)
            else:
                data = np.where(data == src_nanvalue, 0, data)

            if mask_src_nanvalue is None:
                pass
            elif np.isnan(mask_src_nanvalue):
                mask_data = np.where(np.isnan(mask_data), 0, mask_data)
            else:
                mask_data = np.where(
                    mask_data == mask_src_nanvalue, 0, mask_data
                )

            if np.all(mask_data == 0):
                return areas_by_class
            window_transform = src.window_transform(window)

            polygon_mask = rasterize(
                [polygon_geom],
                out_shape=data.shape,
                transform=window_transform,
                fill=0,
                default_value=1,
                dtype=np.uint8,
            )

            combined_mask = (polygon_mask == 1) & (mask_data == 1)
            masked_data = np.where(combined_mask, data, np.nan)

            pixel_area_ha = _get_raster_pixel_area_ha(
                window_transform, src.crs
            )

            valid_data = masked_data[masked_data > 0]
            if len(valid_data) == 0:
                return {}

            unique_values, counts = np.unique(valid_data, return_counts=True)

            for value, pixel_count in zip(unique_values, counts):
                area_ha = float(pixel_count * pixel_area_ha)

                if value in value_to_class:
                    class_key = value_to_class[value]
                    areas_by_class[class_key] = area_ha
                else:
                    areas_by_class[str(int(value))] = area_ha

    return areas_by_class


def get_one_raster_average(
    raster_path: str,
    polygon: geometries.MultiPolygon,
) -> float:
    """
    Calculate average in a given polygon.
    """
    masked_data, _, nodata = _crop_raster_by_polygon(raster_path, polygon)
    if nodata is not None:
        masked_data = np.where(masked_data == nodata, np.nan, masked_data)
    average_value = float(np.nanmean(masked_data))

    return average_value


def get_one_raster_areas_by_category(
    raster_path: str,
    polygon: geometries.MultiPolygon,
    categories: Dict[int, str],
) -> Dict[str, float]:
    """
    Calculate the area in hectares of raster values within a given polygon,
    grouped by user-defined categories.
    """
    masked_data, window_transform, nodata = _crop_raster_by_polygon(
        raster_path, polygon
    )
    if nodata is not None:
        masked_data = np.where(masked_data == nodata, 0, masked_data)

    categories[0] = "No Protegida"
    pixel_area_ha = _get_raster_pixel_area_ha(window_transform, "EPSG:4326")
    unique_values, counts = np.unique(masked_data, return_counts=True)
    areas_by_category = {
        category_key: 0.0 for category_key in categories.values()
    }
    for value, pixel_count in zip(unique_values, counts):
        area_ha = float(pixel_count * pixel_area_ha)
        cat = categories.get(value)

        if cat is not None:
            areas_by_category[cat] = areas_by_category[cat] + area_ha

    return areas_by_category


def get_two_raster_areas_by_category(
    raster1_path: str,
    raster2_path: str,
    polygon: geometries.MultiPolygon,
    categories: Dict[int, str],
) -> Dict[str, float]:
    """
    Calculate the area in hectares of raster values within a given polygon,
    grouped by user-defined categories.
    """
    data, mask_data, window_transform, polygon_geom = (
        crop_two_rasters_by_polygon(
            raster_path=raster1_path,
            mask_raster_path=raster2_path,
            polygon=polygon,
        )
    )

    polygon_mask = rasterize(
        [polygon_geom],
        out_shape=data.shape,
        transform=window_transform,
        fill=0,
        default_value=1,
        dtype=np.uint8,
    )

    mask_binary = mask_data > 0
    combined_mask = (polygon_mask == 1) & mask_binary
    masked_data = np.where(combined_mask, data, np.nan)

    with rasterio.open(raster1_path) as src:
        nodata = src.nodata

    if nodata is not None:
        masked_data = np.where(masked_data == nodata, 0, masked_data)

    categories[0] = "No Protegida"
    pixel_area_ha = _get_raster_pixel_area_ha(window_transform, "EPSG:4326")
    unique_values, counts = np.unique(masked_data, return_counts=True)
    areas_by_category = {
        category_key: 0.0 for category_key in categories.values()
    }
    for value, pixel_count in zip(unique_values, counts):
        area_ha = float(pixel_count * pixel_area_ha)
        cat = categories.get(value)

        if cat is not None:
            areas_by_category[cat] = areas_by_category[cat] + area_ha

    return areas_by_category


def get_frequency_histogram(
    raster_path: str,
    polygon: geometries.MultiPolygon,
    bins: int = 20,
    data_range: Tuple[float, float] = (0, 1),
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate the frequency histogram of raster values within a given polygon.
    """
    
    masked_data, _, nodata = _crop_raster_by_polygon(raster_path, polygon)
    if nodata is not None:
        masked_data = np.where(masked_data == nodata, np.nan, masked_data)
        
    valid_data = masked_data[~np.isnan(masked_data)]
    if valid_data.size == 0:
        raise ValueError("No valid data found in the polygon region.")

    hist, bin_edges = np.histogram(valid_data, bins=bins, range=data_range)
    return hist, bin_edges


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    if hex_color.startswith("#"):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            return r, g, b, 255
        else:
            raise ValueError(f"Invalid hex color format: {hex_color}")
    raise ValueError(f"Hex color must start with '#': {hex_color}")


def crop_two_rasters_by_polygon(
    raster_path: str,
    mask_raster_path: str,
    polygon: geometries.MultiPolygon,
) -> Tuple[
    np.ndarray, np.ndarray, rasterio.Affine, ShapelyPolygon | MultiPolygon
]:
    polygon_geom_raw = shape(polygon)
    if isinstance(polygon_geom_raw, (ShapelyPolygon, MultiPolygon)):
        polygon_geom = polygon_geom_raw
    else:
        raise UnprocessableError(
            code=422,
            usr_msg="Invalid polygon geometry.",
            e=Exception(
                f"Expected Polygon or MultiPolygon, got {type(polygon_geom_raw)}"
            ),
        )

    with (
        rasterio.open(raster_path) as src,
        rasterio.open(mask_raster_path) as mask_src,
    ):
        if src.crs != mask_src.crs:
            raise ValueError(
                "Raster coordinate reference systems do not match."
            )
        if src.res != mask_src.res:
            raise ValueError("Raster resolutions do not match.")

        minx, miny, maxx, maxy = polygon_geom.bounds
        window = from_bounds(minx, miny, maxx, maxy, src.transform)
        window_mask = from_bounds(minx, miny, maxx, maxy, mask_src.transform)

        data = src.read(1, window=window)
        mask_data = mask_src.read(1, window=window_mask)

        data = np.where(np.isnan(data), 0, data)

        mask_data = np.where(np.isnan(mask_data), 0, mask_data)

        window_transform = src.window_transform(window)
        return data, mask_data, window_transform, polygon_geom


def get_two_raster_image(
    raster_path: str,
    mask_raster_path: str,
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

    try:
        data, mask_data, window_transform, polygon_geom = (
            crop_two_rasters_by_polygon(
                raster_path=raster_path,
                mask_raster_path=mask_raster_path,
                polygon=polygon,
            )
        )

        polygon_mask = rasterize(
            [polygon_geom],
            out_shape=data.shape,
            transform=window_transform,
            fill=0,
            default_value=1,
            dtype=np.uint8,
        )

        mask_binary = mask_data > 0
        combined_mask = (polygon_mask == 1) & mask_binary
        masked_data = np.where(combined_mask, data, np.nan)

        if len(masked_data) == 0 or np.all(masked_data != class_value):
            raise NotFoundError(
                usr_msg="No data available for the selected class.",
                log_msg=(
                    f"No data generated for class value {class_value} "
                    "after applying polygon + mask raster intersection."
                ),
            )

        h, w = masked_data.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        rgba[masked_data == class_value] = colormap[class_value]

        pil_image = Image.fromarray(rgba, mode="RGBA")
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        del data, mask_data, polygon_mask, mask_binary, combined_mask
        del masked_data, rgba, img_buffer, pil_image
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error rendering class value {class_value}: {str(e)}"
        )
        raise ServerError(
            code=500,
            usr_msg="There was an error processing the requested class.",
            e=e,
        )
    finally:
        gc.collect()

    return img_base64
