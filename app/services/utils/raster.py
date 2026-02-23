import base64
import io

from PIL import Image
from rio_tiler.io.rasterio import Reader
import numpy as np
from typing import Dict, List, Tuple, cast
from shapely import box
from shapely.geometry import shape
from shapely.ops import transform as shapely_transform
import rasterio
from rasterio.crs import CRS
from rasterio.mask import mask
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Polygon as ShapelyPolygon

from geojson_pydantic import geometries
from app.middleware.log_middleware import logger
from app.utils.errors import NotFoundError, ServerError


def crop_raster(
    raster_path: str,
    polygon,
    category: int,
    values: List[int],
    colors: List[str],
) -> str:
    Image.MAX_IMAGE_PIXELS = None

    colormap: Dict[int, Tuple[int, int, int, int]] = {
        value: hex_to_rgba(color) for value, color in zip(values, colors)
    }

    if category not in colormap:
        raise NotFoundError(
            usr_msg="Selected category is not available in values.",
            log_msg=f"Category {category} not found in values.",
        )

    try:
        with Reader(input=raster_path, options={}) as image:
            img = image.feature(polygon)

            color = colormap[category]

            rendered_img = img.render(
                add_mask=True, colormap={category: color}
            )

            if not rendered_img:
                raise NotFoundError(
                    usr_msg="No data available for the selected category.",
                    log_msg=f"No data generated for category {category}.",
                )

            pil_image = Image.open(io.BytesIO(rendered_img))
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            img_base64 = base64.b64encode(img_buffer.getvalue()).decode(
                "utf-8"
            )

    except Exception as e:
        logger.error(
            f"Unexpected error rendering category {category}: {str(e)}"
        )
        raise ServerError(
            code=500,
            usr_msg=f"There was an error processing category {category}.",
            e=e,
        )

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
            return {}

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

        if len(valid_data) == 0:
            return {}

        unique_values, counts = np.unique(valid_data, return_counts=True)

        value_to_category = {val: name for name, val in categories.items()}

        areas_by_category = {}
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
            return 0.0

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
