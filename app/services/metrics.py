from typing import Dict, List
from geojson_pydantic import geometries
from fastapi import HTTPException

from app.services.utils.raster import (
    get_one_raster_image,
    get_one_raster_areas,
    get_one_raster_average,
    get_two_raster_areas,
)
from app.services.utils.stac import (
    get_item_resolution,
    get_item_index_by_resolution,
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.services.utils.stac import fetch_collection_metadata

from app.models.models import Metric, Collection
from app.persistence.polygon_metric_layer_persistence import (
    get_existing_layer,
    create_polygon_metric_layer,
)
from app.persistence.polygon_persistence import get_polygon_by_id
from app.persistence.polygon_metric_persistence import (
    create_polygon_metric,
    get_polygon_metric,
)
from app.persistence.metric_persistence import (
    get_metric_by_name,
)

from app.utils.s3_utils import upload_to_s3
from app.utils.errors import ServerError, MetadataError


async def get_or_create_polygon_metric(
    polygon_id: int, metric_name: str
) -> List[Dict[str, str | float]] | Dict[str, str | float]:
    """
    Checks if metric values already exist for the given polygon and metric.
    If they exist, return them. Otherwise, calculate, persist, and return.
    """

    polygon_obj = await get_polygon_by_id(polygon_id)

    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    metric_obj = await get_metric_by_name(metric_name)

    if not metric_obj:
        raise HTTPException(
            status_code=400, detail="Metric not found in database"
        )

    polygon_metric = await get_polygon_metric(polygon_obj, metric_obj)

    if polygon_metric:
        return polygon_metric.values

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    primary_collection = next(
        (mc for mc in metric_obj.collections if mc.is_primary), None
    )
    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric_name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")

    values = await OperationFunctions(
        metric_obj.operation_type
    ).values_function(primary_collection.collection, metric_obj, polygon)

    await create_polygon_metric(polygon_obj, metric_obj, values)
    return values


async def get_or_create_polygon_metric_layer(
    metric_name: str, polygon_id: int, item_id: str, class_id: str
) -> Dict[str, str]:
    """
    Checks if the layer already exists. If not, generates it, saves and returns the URL.
    """
    polygon_obj = await get_polygon_by_id(polygon_id)

    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    metric_obj = await get_metric_by_name(metric_name)

    if not metric_obj:
        raise HTTPException(
            status_code=400, detail="Metric not found in database"
        )
    if not metric_obj.has_layer:
        raise HTTPException(
            status_code=501, detail="Metric doesn't have an associated layer"
        )

    existing_layer = await get_existing_layer(
        metric_obj, polygon_obj, class_id, item_id
    )

    if existing_layer:
        return {"layer": existing_layer.layer_url}

    primary_collection = next(
        (mc for mc in metric_obj.collections if mc.is_primary), None
    )
    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric_obj.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    calculate_layer_func = OperationFunctions(
        metric_obj.operation_type
    ).layer_function

    if calculate_layer_func is None:
        raise HTTPException(
            status_code=501, detail="Metric doesn't have an associated layer"
        )

    img_base64 = await calculate_layer_func(
        polygon,
        primary_collection.collection,
        item_id,
        class_id,
    )
    image_url = await upload_to_s3(
        image_data=img_base64,
        filename=f"{metric_name}_{polygon_id}_{item_id}_{class_id}.png",
        content_type="image/png",
    )

    await create_polygon_metric_layer(
        metric_obj=metric_obj,
        polygon_obj=polygon_obj,
        class_id=class_id,
        item_id=item_id,
        image_url=image_url,
    )

    return {"layer": image_url}


async def calculate_single_coll_values(
    primary_collection: Collection, _, polygon: geometries.MultiPolygon
) -> Dict[str, str | float]:
    """
    Calculate values for a metric that uses only the first item from one collection,
    grouped by the collection categories
    """
    categories, _, _ = await fetch_collection_metadata(primary_collection)

    id, raster_url = get_items_asset_url(primary_collection.name)[0]

    raster_values = get_one_raster_areas(raster_url, polygon, categories)

    return {"id": id, **raster_values}


async def calculate_single_coll_all_items_values(
    primary_collection: Collection, _, polygon: geometries.MultiPolygon
) -> List[Dict[str, str | float]]:
    """
    Calculate values for a metric that uses all items from one collection,
    grouped by the collection categories
    """

    categories, _, _ = await fetch_collection_metadata(primary_collection)

    rasters_info = get_items_asset_url(primary_collection.name)
    result = []
    for id, url in rasters_info:
        raster_values = get_one_raster_areas(url, polygon, categories)

        result.append({"id": id, **raster_values})

    return result


async def calculate_two_colls_values(
    primary_collection: Collection,
    metric: Metric,
    polygon: geometries.MultiPolygon,
) -> Dict[str, str | float]:
    """
    Calculate values for a metric that uses only the first item from two collections.
    The values are grouped by the categories of the primary collection.
    """

    secondary_collection = next(
        (mc for mc in metric.collections if not mc.is_primary), None
    )
    if secondary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Secondary collection not found"),
        )

    await secondary_collection.fetch_related("collection")

    categories, _, _ = await fetch_collection_metadata(primary_collection)

    secondary_collection = secondary_collection.collection

    id_pri, raster_pri_url = get_items_asset_url(primary_collection.name)[0]
    resol_pri = get_item_resolution(primary_collection.name, 0)

    index_sec = get_item_index_by_resolution(
        secondary_collection.name, resol_pri
    )
    _, raster_sec_url = get_items_asset_url(secondary_collection.name)[
        index_sec
    ]
    raster_values = get_two_raster_areas(
        raster_pri_url, raster_sec_url, polygon, categories
    )

    return {"id": id_pri, **raster_values}


async def calculate_ave_coll_values(
    primary_collection: Collection, _, polygon: geometries.MultiPolygon
) -> Dict[str, str | float]:
    """
    calculates the average of the values from a collection within a polygon
    """
    id, raster_url = get_items_asset_url(primary_collection.name)[0]
    average = get_one_raster_average(raster_url, polygon)

    return {"id": id, "average": average}


def calculate_ave_multiple_colls_values():
    pass


def calculate_cat_single_coll_values():
    pass


def calculate_cat_two_colls_values():
    pass


def calculate_cat_single_coll_filtered_values():
    pass


async def calculate_single_coll_layer(
    polygon: geometries.MultiPolygon,
    primary_collection: Collection,
    item_id: str,
    class_id: str,
) -> str:
    """
    Get the layer for a metric that uses only one collection
    """
    classes_map, values, colors = await fetch_collection_metadata(
        primary_collection
    )

    if class_id not in classes_map:
        raise MetadataError(
            code=404,
            log_msg=f"class_id {class_id} doesn't exist in metric",
            usr_msg=f"class_id {class_id} doesn't exist in metric",
        )

    raster_href = get_asset_href_by_item_id(primary_collection.name, item_id)

    image_base64 = get_one_raster_image(
        raster_path=raster_href,
        polygon=polygon,
        class_value=classes_map[class_id],
        values=values,
        colors=colors,
    )

    return image_base64


def calculate_two_colls_layer():
    pass


def calculate_cat_single_coll_filtered_layer():
    pass


class OperationFunctions:
    def __init__(self, operation):
        values_functions = {
            "AREA_SINGLE-COLLECTION": calculate_single_coll_values,
            "AREA_SINGLE-COLLECTION_ALL-ITEMS": calculate_single_coll_all_items_values,
            "AREA_TWO-COLLECTIONS": calculate_two_colls_values,
            "AVERAGE_SINGLE-COLLECTION": calculate_ave_coll_values,
            "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS": calculate_ave_multiple_colls_values,
            "AREA_CATEGORIES_SINGLE-COLLECTION": calculate_cat_single_coll_values,
            "AREA_CATEGORIES_TWO-COLLECTIONS": calculate_cat_two_colls_values,
            "AREA_CATEGORIES_SINGLE-COLLECTION_FILTERED": calculate_cat_single_coll_filtered_values,
        }
        layer_functions = {
            "AREA_SINGLE-COLLECTION": calculate_single_coll_layer,
            "AREA_SINGLE-COLLECTION_ALL-ITEMS": calculate_single_coll_layer,
            "AREA_TWO-COLLECTIONS": calculate_two_colls_layer,
            "AREA_CATEGORIES_SINGLE-COLLECTION_FILTERED": calculate_cat_single_coll_filtered_layer,
        }
        self.values_function = values_functions[operation]
        self.layer_function = (
            layer_functions[operation]
            if operation in layer_functions
            else None
        )
