from enum import Enum
from typing import Dict, List
from geojson_pydantic import geometries
from fastapi import HTTPException

from app.routes.schemas.LayerResponse import LayerResponse

from app.services.utils.raster import (
    crop_raster,
    get_one_raster_areas,
    get_one_raster_average,
)
from app.services.utils.stac import (
    get_items_asset_url,
    get_asset_href_by_item_id,
)
from app.services.utils.stac import fetch_collection_metadata

from app.models.models import Metric, Polygon, PolygonMetric
from app.persistence.layer_persistence import (
    get_existing_layer,
    save_layer_record,
)
from app.persistence.polygon_persistence import get_polygon_by_id
from app.persistence.polygon_metric_persistence import create_polygon_metric
from app.persistence.metric_persistence import (
    get_metric_by_name,
)

from app.utils.s3_utils import upload_to_s3
from app.utils.errors import ServerError, UnprocessableError


async def get_or_create_polygon_metric(
    polygon_id: int, metric_name: str
) -> List[dict] | Dict:
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

    polygon_metric = await PolygonMetric.get_or_none(
        polygon=polygon_obj, metric=metric_obj
    )

    if polygon_metric:
        return polygon_metric.values

    polygon = geometries.MultiPolygon(**polygon_obj.geometry)

    values = await OperationEnum(metric_obj.operation_type).function(
        metric_obj, polygon
    )
    await create_polygon_metric(polygon_obj, metric_obj, values)
    return values


async def get_or_create_layer_by_polygon(
    metric_name: str, polygon_id: int, item_id: str, category: int
) -> LayerResponse:
    """
    Checks if the layer already exists. If not, generates it, saves and returns the URL.
    """
    # TODO: Cambiar para que funcione de acuerdo al tipo de operación
    metric_obj = await get_metric_by_name(metric_name)

    if not metric_obj:
        raise HTTPException(
            status_code=400, detail="Metric not found in database"
        )

    polygon_obj = await Polygon.get_or_none(id=polygon_id)

    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    existing_item = await get_existing_layer(
        metric_obj.id, polygon_id, category, item_id
    )

    if existing_item:
        return LayerResponse(layer=existing_item.layer_url)

    primary_collection = next(
        mc for mc in metric_obj.collections if mc.is_primary
    )
    await primary_collection.fetch_related("collection")

    (
        _,
        values,
        colors,
    ) = await fetch_collection_metadata(primary_collection.collection)
    raster_href = get_asset_href_by_item_id(
        primary_collection.collection, item_id
    )

    image_base64 = crop_raster(
        raster_path=raster_href,
        polygon=polygon_obj.geometry,
        category=category,
        values=values,
        colors=colors,
    )

    image_url = await upload_to_s3(
        image_data=image_base64,
        filename=f"{metric_name}_{polygon_id}_{item_id}_{category}.png",
        content_type="image/png",
    )

    await save_layer_record(
        metric_obj=metric_obj,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        image_url=image_url,
    )

    return LayerResponse(layer=image_url)


async def calculate_single_coll(
    metric: Metric, polygon: geometries.MultiPolygon
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

    categories, _, _ = await fetch_collection_metadata(
        primary_collection.collection
    )

    id, raster_url = get_items_asset_url(primary_collection.collection.name)[0]

    try:
        raster_values = get_one_raster_areas(raster_url, polygon, categories)
    except UnprocessableError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.usr_msg,
        )

    return {"id": id, **raster_values}


async def calculate_single_coll_all_items(
    metric: Metric, polygon: geometries.MultiPolygon
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

    categories, _, _ = await fetch_collection_metadata(
        primary_collection.collection
    )

    rasters_info = get_items_asset_url(primary_collection.collection.name)
    result = []
    for id, url in rasters_info:
        try:
            raster_values = get_one_raster_areas(url, polygon, categories)
        except UnprocessableError as e:
            raise HTTPException(
                status_code=e.code,
                detail=e.usr_msg,
            )

        result.append({"id": id, **raster_values})

    return result


async def calculate_two_colls(
    metric: Metric, polygon: geometries.MultiPolygon
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

    categories, _, _ = await fetch_collection_metadata(
        primary_collection.collection
    )

    # TODO: Cuando haya collecciones de EE separados ajustar esta implementación,
    # solo dejé de aquí para arriba porque ninguna otra de las que están listas
    # para probar usaba las colecciones secundarias
    id, raster_url = get_items_asset_url(primary_collection.collection.name)[0]

    try:
        raster_values = get_one_raster_areas(raster_url, polygon, categories)
    except UnprocessableError as e:
        raise HTTPException(status_code=e.code, detail=e.usr_msg)

    return {"id": id, **raster_values}


async def calculate_ave_coll(
    metric: Metric, polygon: geometries.MultiPolygon
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
    id, raster_url = get_items_asset_url(primary_collection.collection.name)[0]
    try:
        average = get_one_raster_average(raster_url, polygon)
    except UnprocessableError as e:
        raise HTTPException(
            status_code=e.code,
            detail=e.usr_msg,
        )
    return {"id": id, "average": average}


def calculate_ave_multiple_colls():
    pass


def calculate_pa():
    pass


def calculate_pa_single_coll():
    pass


def calculate_pa_single_coll_filtered():
    pass


class OperationEnum(Enum):
    AREA_SINGLE_COLLECTION = "AREA_SINGLE-COLLECTION"
    AREA_SINGLE_COLLECTION_ALL_ITEMS = "AREA_SINGLE-COLLECTION_ALL-ITEMS"
    AREA_TWO_COLLECTIONS = "AREA_TWO-COLLECTIONS"
    AVERAGE_SINGLE_COLLECTION = "AVERAGE_SINGLE-COLLECTION"
    AVERAGE_MULTIPLE_COLLECTION_ALL_ITEMS = (
        "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS"
    )
    PA = "PA"
    PA_SINGLE_COLLECTION = "PA_SINGLE-COLLECTION"
    PA_SINGLE_COLLECTION_FILTERED = "PA_SINGLE-COLLECTION-FILTERED"

    def __init__(self, value):
        functions = {
            "AREA_SINGLE-COLLECTION": calculate_single_coll,
            "AREA_SINGLE-COLLECTION_ALL-ITEMS": calculate_single_coll_all_items,
            "AREA_TWO-COLLECTIONS": calculate_two_colls,
            "AVERAGE_SINGLE-COLLECTION": calculate_ave_coll,
            "AVERAGE_MULTIPLE-COLLECTION_ALL-ITEMS": calculate_ave_multiple_colls,
            "PA": calculate_pa,
            "PA_SINGLE-COLLECTION": calculate_pa_single_coll,
            "PA_SINGLE-COLLECTION-FILTERED": calculate_pa_single_coll_filtered,
        }
        self.function = functions[value]
