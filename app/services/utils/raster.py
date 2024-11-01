import base64
import io

from PIL import Image
from rasterstats import zonal_stats
from rio_tiler.io.rasterio import Reader
import numpy as np
import geopandas as gpd
from typing import Any, Dict
import rioxarray
from shapely import geometry
from app.middleware.log_middleware import logger
from app.utils.errors import NotFoundError, ServerError


# TODO: define how to get the color map (db, object, etc), it can't be hardcoded here
def crop_raster(raster_path: str, polygon, category: int) -> Dict[str, str]:
    Image.MAX_IMAGE_PIXELS = None
    base64_images = {}

    colormap = {
        0: (255, 0, 0, 255),
        1: (128, 204, 102, 255),
        2: (232, 214, 107, 255),
    }

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

            base64_images[str(category)] = img_base64

    except Exception as e:

        logger.error(
            f"Unexpected error rendering category {category}: {str(e)}"
        )

        raise ServerError(
            code=500,
            usr_msg=f"There was an error processing category {category}.",
            e=e,
        )

    return base64_images


# TODO: verify if categories should be kept as object or if it should be get from the db
def get_raster_values(
    raster_path: str, polygon: geometry.Polygon, categories: Dict[str, int]
) -> Dict[str, Any]:
    gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="EPSG:4326")
    target_crs = "EPSG:9377"

    raster = rioxarray.open_rasterio(raster_path, masked=True)

    clipped_raster = raster.rio.clip(gdf.geometry, from_disk=True)

    if clipped_raster.rio.crs != target_crs:
        clipped_raster = clipped_raster.rio.reproject(target_crs)

    if gdf.crs != target_crs:
        gdf = gdf.to_crs(target_crs)

    stats = zonal_stats(
        gdf,
        clipped_raster.values[0],  # use raster first band
        affine=clipped_raster.rio.transform(),
        categorical=True,
        nodata=np.nan,
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
