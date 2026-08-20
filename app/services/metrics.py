import re
import unicodedata
from typing import Dict, List
from geojson_pydantic import geometries
from fastapi import HTTPException

from app.services.utils.raster import (
    get_one_raster_areas_by_category,
    get_two_raster_areas_by_category,
    get_one_raster_image,
    get_one_raster_areas_by_classes,
    get_one_raster_average,
    get_two_raster_areas_by_classes,
    get_two_raster_image,
    get_frequency_histogram,
    get_polygon_and_mask_averages,
    get_one_raster_gradient_image,
)
from app.services.utils.stac import (
    get_item_index_by_resolution,
    get_items_asset_url,
    get_asset_href_by_item_id,
    get_item_resolution_by_item_id,
)
from app.services.utils.stac import fetch_collection_metadata

from app.models.models import Metric, Collection, Polygon
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
from app.persistence.indicator_persistence import AbstractIndicator

from app.utils.s3_utils import upload_to_s3
from app.utils.errors import ServerError, MetadataError
from app.persistence.utils.lock_utils import advisory_xact_lock


async def _is_national_polygon(polygon_obj: Polygon) -> bool:
    await polygon_obj.fetch_related("area_type")
    return polygon_obj.area_type.id == "national"


async def get_or_create_polygon_metric(
    polygon_id: int,
    metric_name: str,
    group: str | None = None,
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

    if (
        await _is_national_polygon(polygon_obj)
        and not metric_obj.allows_national
    ):
        raise HTTPException(
            status_code=404,
            detail="Metric not available for national area",
        )

    if metric_obj.has_group and group is None:
        raise HTTPException(
            status_code=422,
            detail="group is required for this metric",
        )

    async with advisory_xact_lock(
        "polygon_metric", str(polygon_obj.id), str(metric_obj.id)
    ) as connection:
        operation_functions = OperationFunctions(metric_obj.operation_type)
        polygon_metric = await get_polygon_metric(
            polygon_obj, metric_obj, db=connection
        )

        if polygon_metric is not None:
            return polygon_metric.values

        values = await operation_functions.calculate_values(
            metric_obj, polygon_obj, group
        )

        await create_polygon_metric(
            polygon_obj, metric_obj, values, db=connection
        )
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

    if (
        await _is_national_polygon(polygon_obj)
        and not metric_obj.allows_national
    ):
        raise HTTPException(
            status_code=404,
            detail="Metric not available for national area",
        )

    calculate_layer_func = OperationFunctions(
        metric_obj.operation_type
    ).layer_function

    if calculate_layer_func is None:
        raise HTTPException(
            status_code=501, detail="Metric doesn't have an associated layer"
        )

    async with advisory_xact_lock(
        "polygon_metric_layer",
        str(metric_obj.id),
        str(polygon_obj.id),
        item_id,
        class_id,
    ) as connection:
        existing_layer = await get_existing_layer(
            metric_obj, polygon_obj, class_id, item_id, db=connection
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

        img_base64 = await calculate_layer_func(
            polygon,
            primary_collection.collection,
            item_id,
            class_id,
            metric_obj,
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
            db=connection,
        )

        return {"layer": image_url}


"""
SPECIFIC VALUES FUNCTIONS
"""


async def calculate_single_coll_values(
    metric: Metric, polygon_obj: Polygon
) -> Dict[str, str | float]:
    """
    Calculate values for a metric that uses only the first item from one collection,
    grouped by the collection categories
    """

    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection
    classes_map, _, _, _, _ = await fetch_collection_metadata(
        primary_collection
    )

    id, raster_url = get_items_asset_url(primary_collection.name)[0]

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    raster_values = get_one_raster_areas_by_classes(
        raster_url, polygon, classes_map
    )

    return {"id": id, **raster_values}


async def calculate_single_coll_all_items_values(
    metric: Metric, polygon_obj: Polygon
) -> List[Dict[str, str | float]]:
    """
    Calculate values for a metric that uses all items from one collection,
    grouped by the collection categories
    """
    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

    classes_map, _, _, _, _ = await fetch_collection_metadata(
        primary_collection
    )

    rasters_info = get_items_asset_url(primary_collection.name)
    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    result = []
    for id, url in rasters_info:
        raster_values = get_one_raster_areas_by_classes(
            url, polygon, classes_map
        )

        result.append({"id": id, **raster_values})

    return result


async def calculate_two_colls_values(
    metric: Metric,
    polygon_obj: Polygon,
) -> Dict[str, str | float]:
    """
    Calculate values for a metric that uses only the first item from two collections.
    The values are grouped by the categories of the primary collection.
    """
    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

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

    classes_map, _, _, _, _ = await fetch_collection_metadata(
        primary_collection
    )

    secondary_collection = secondary_collection.collection

    id_pri, raster_pri_url = get_items_asset_url(primary_collection.name)[0]
    resol_pri = get_item_resolution_by_item_id(primary_collection.name, id_pri)

    index_sec = get_item_index_by_resolution(
        secondary_collection.name, resol_pri
    )
    _, raster_sec_url = get_items_asset_url(secondary_collection.name)[
        index_sec
    ]
    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    raster_values = get_two_raster_areas_by_classes(
        raster_pri_url, raster_sec_url, polygon, classes_map
    )

    return {"id": id_pri, **raster_values}


async def calculate_ave_coll_values(
    metric: Metric, polygon_obj: Polygon
) -> Dict[str, str | float]:
    """
    calculates the average of the values from a collection within a polygon
    """
    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

    id, raster_url = get_items_asset_url(primary_collection.name)[0]
    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    average = get_one_raster_average(raster_url, polygon)

    return {"id": id, "average": average}


async def calculate_ave_multiple_colls_values(
    metric: Metric, polygon_obj: Polygon
) -> List[Dict[str, str | float]]:
    """
    Calculates, for each primary item, the average in the full polygon and
    intersections with all configured secondary collections.
    """
    primary_metric_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )
    if primary_metric_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_metric_collection.fetch_related("collection")
    primary_collection = primary_metric_collection.collection

    secondary_metric_collections = [
        mc for mc in metric.collections if not mc.is_primary
    ]

    for sec_metric_collection in secondary_metric_collections:
        await sec_metric_collection.fetch_related("collection")

    secondary_collections = [
        mc.collection for mc in secondary_metric_collections
    ]
    secondary_keys = [collection.name for collection in secondary_collections]

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    results: List[Dict[str, str | float]] = []

    for item_id, raster_url in get_items_asset_url(primary_collection.name):
        item_res = get_item_resolution_by_item_id(
            primary_collection.name, item_id
        )
        mask_rasters: Dict[str, str] = {}

        for result_key, mask_collection in zip(
            secondary_keys, secondary_collections
        ):
            mask_index = get_item_index_by_resolution(
                mask_collection.name, item_res
            )
            _, mask_raster_url = get_items_asset_url(mask_collection.name)[
                mask_index
            ]
            mask_rasters[result_key] = mask_raster_url

        averages = get_polygon_and_mask_averages(
            raster_path=raster_url,
            polygon=polygon,
            mask_rasters=mask_rasters,
        )

        result: Dict[str, str | float] = {
            "id": item_id,
            "poligono": averages["average"],
        }
        for result_key in secondary_keys:
            result[result_key] = averages[result_key]
        results.append(result)

    return results


async def calculate_cat_single_coll_values(
    metric: Metric, polygon_obj: Polygon
) -> Dict[str, str | float]:
    """
    calculates the area of each category of a collection within a polygon
    """
    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

    _, values, _, _, categories = await fetch_collection_metadata(
        primary_collection
    )

    values_by_category = {
        value: category for value, category in zip(values, categories)
    }
    id, raster_url = get_items_asset_url(primary_collection.name)[0]

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    raster_values = get_one_raster_areas_by_category(
        raster_url, polygon, values_by_category
    )

    return {"id": id, **raster_values}


async def calculate_cat_two_colls_values(
    metric: Metric, polygon_obj: Polygon
) -> Dict[str, str | float]:
    """
    calculates the area of each category of a collection within a polygon
    croped by a second collection
    """
    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

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

    _, values, _, _, categories = await fetch_collection_metadata(
        primary_collection
    )

    values_by_category = {
        value: category for value, category in zip(values, categories)
    }

    secondary_collection = secondary_collection.collection

    id_pri, raster_pri_url = get_items_asset_url(primary_collection.name)[0]
    resol_pri = get_item_resolution_by_item_id(primary_collection.name, id_pri)

    index_sec = get_item_index_by_resolution(
        secondary_collection.name, resol_pri
    )
    _, raster_sec_url = get_items_asset_url(secondary_collection.name)[
        index_sec
    ]
    polygon = geometries.MultiPolygon(**polygon_obj.geometry)
    raster_values = get_two_raster_areas_by_category(
        raster_pri_url, raster_sec_url, polygon, values_by_category
    )

    return {"id": id_pri, **raster_values}


async def calculate_frequency_values(
    metric: Metric, polygon_obj: Polygon
) -> Dict[str, str | list[float] | list[int]]:
    """
    calculates the frequency of values from a collection within a polygon
    """

    primary_collection = next(
        (mc for mc in metric.collections if mc.is_primary), None
    )

    if primary_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Primary collection not found"),
        )

    await primary_collection.fetch_related("collection")
    primary_collection = primary_collection.collection

    id, raster_url = get_items_asset_url(primary_collection.name)[0]
    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    hist, bin_edges = get_frequency_histogram(
        raster_path=raster_url, polygon=polygon, bins=20, data_range=(0, 1)
    )

    return {
        "id": id,
        "frequency": hist.tolist(),
        "bin_edges": bin_edges.tolist(),
    }


def calculate_cat_single_coll_filtered_values():
    pass


async def calculate_table_precalculated_values(
    metric: Metric,
    polygon_obj: Polygon,
    group: str | None = None,
    has_group: bool = False,
) -> Dict[str, str | float] | List[Dict[str, str | float]]:
    """
    Queries the results for the precalculated indicators
    """
    indicator = next(iter(metric.indicator), None)
    if indicator is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Indicator not found"),
        )

    query_obj = AbstractIndicator(indicator.indicator)
    if has_group:
        return await query_obj.get_values_by_polygon(
            polygon=polygon_obj, has_group=has_group
        )
    return await query_obj.get_values_by_polygon(
        polygon=polygon_obj, group=group, has_group=has_group
    )


"""
SPECIFIC LAYER FUNCTIONS
"""


async def calculate_single_coll_layer(
    polygon: geometries.MultiPolygon,
    primary_collection: Collection,
    item_id: str,
    class_id: str,
    metric: Metric | None = None,
) -> str:
    """
    Get the layer for a metric that uses only one collection
    """
    classes_map, values, _, colors, _ = await fetch_collection_metadata(
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


async def calculate_two_colls_layer(
    polygon: geometries.MultiPolygon,
    primary_collection: Collection,
    item_id: str,
    class_id: str,
    metric: Metric | None = None,
) -> str:
    """
    Get the layer for a metric that uses two collections.
    """
    classes_map, values, _, colors, _ = await fetch_collection_metadata(
        primary_collection
    )

    if class_id not in classes_map:
        raise MetadataError(
            code=404,
            log_msg=f"class_id {class_id} doesn't exist in metric",
            usr_msg=f"class_id {class_id} doesn't exist in metric",
        )

    if metric is None:
        raise ServerError(
            code=500,
            usr_msg="There was an internal error processing the request.",
            e=Exception("Missing metric context for AREA_TWO-COLLECTIONS"),
        )

    secondary_metric_collection = next(
        (mc for mc in metric.collections if not mc.is_primary), None
    )
    if secondary_metric_collection is None:
        raise ServerError(
            code=500,
            usr_msg=f"There was an error calculating the metric {metric.name}.",
            e=Exception("Secondary collection not found"),
        )

    await secondary_metric_collection.fetch_related("collection")
    secondary_collection = secondary_metric_collection.collection

    primary_raster_href = get_asset_href_by_item_id(
        primary_collection.name, item_id
    )
    primary_res = get_item_resolution_by_item_id(
        primary_collection.name, item_id
    )

    index_sec = get_item_index_by_resolution(
        secondary_collection.name, primary_res
    )
    _, secondary_raster_href = get_items_asset_url(secondary_collection.name)[
        index_sec
    ]

    image_base64 = get_two_raster_image(
        raster_path=primary_raster_href,
        mask_raster_path=secondary_raster_href,
        polygon=polygon,
        class_value=classes_map[class_id],
        values=values,
        colors=colors,
    )

    return image_base64


async def calculate_frequency_layer(
    polygon: geometries.MultiPolygon,
    primary_collection: Collection,
    item_id: str,
    class_id: str,
    metric: Metric | None = None,
) -> str:
    """
    Get the heatmap layer for a metric over a continuous raster.
    There is no discrete class in this operation, so class_id must be the
    metric's own name instead of a class key from /values.
    """
    if metric is None:
        raise ServerError(
            code=500,
            usr_msg="There was an internal error processing the request.",
            e=Exception(
                "Missing metric context for FREQUENCY_SINGLE-COLLECTION"
            ),
        )

    if class_id != metric.name:
        raise MetadataError(
            code=404,
            log_msg=f"class_id {class_id} doesn't match metric name {metric.name}",
            usr_msg=f"class_id {class_id} doesn't exist in metric",
        )

    _, _, _, colors, _ = await fetch_collection_metadata(primary_collection)

    raster_href = get_asset_href_by_item_id(primary_collection.name, item_id)

    image_base64 = get_one_raster_gradient_image(
        raster_path=raster_href,
        polygon=polygon,
        colors=colors,
    )

    return image_base64


def calculate_cat_single_coll_filtered_layer():
    pass


class OperationFunctions:
    def __init__(self, operation):
        self.operation = operation
        values_functions = {
            "AREA_SINGLE-COLLECTION": (
                calculate_single_coll_values,
                False,
            ),
            "AREA_SINGLE-COLLECTION_ALL-ITEMS": (
                calculate_single_coll_all_items_values,
                False,
            ),
            "AREA_TWO-COLLECTIONS": (
                calculate_two_colls_values,
                False,
            ),
            "AVERAGE_SINGLE-COLLECTION": (
                calculate_ave_coll_values,
                False,
            ),
            "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS": (
                calculate_ave_multiple_colls_values,
                False,
            ),
            "AREA_CATEGORIES_SINGLE-COLLECTION": (
                calculate_cat_single_coll_values,
                False,
            ),
            "AREA_CATEGORIES_TWO-COLLECTIONS": (
                calculate_cat_two_colls_values,
                False,
            ),
            "AREA_CATEGORIES_SINGLE-COLLECTION_FILTERED": (
                calculate_cat_single_coll_filtered_values,
                False,
            ),
            "TABLE_PRECALCULATED": (
                calculate_table_precalculated_values,
                True,
            ),
            "FREQUENCY_SINGLE-COLLECTION": (
                calculate_frequency_values,
                False,
            ),
        }
        layer_functions = {
            "AREA_SINGLE-COLLECTION": calculate_single_coll_layer,
            "AREA_SINGLE-COLLECTION_ALL-ITEMS": calculate_single_coll_layer,
            "AREA_TWO-COLLECTIONS": calculate_two_colls_layer,
            "AREA_CATEGORIES_SINGLE-COLLECTION_FILTERED": calculate_cat_single_coll_filtered_layer,
            "FREQUENCY_SINGLE-COLLECTION": calculate_frequency_layer,
        }
        self.values_function, self.values_function_accepts_group = (
            values_functions[operation]
        )
        self.layer_function = (
            layer_functions[operation]
            if operation in layer_functions
            else None
        )

    async def calculate_values(
        self,
        metric: Metric,
        polygon_obj: Polygon,
        group: str | None = None,
    ):
        if self.values_function_accepts_group:
            return await self.values_function(metric, polygon_obj, group)
        return await self.values_function(metric, polygon_obj)
