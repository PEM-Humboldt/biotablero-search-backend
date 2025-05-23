from fastapi import HTTPException

from app.models.models import Polygon
from app.persistence.layer_persistence import (
    get_existing_layer,
    save_layer_record,
)
from app.routes.schemas.MetricResponse import LayerResponse
from app.services.utils.collection import get_asset_href_by_item_id
from app.services.utils.metadata import fetch_collection_metadata
from app.services.utils.raster import crop_raster
from app.utils.s3_utils import upload_to_s3


async def get_layer_by_polygon(
    metric_id: str, polygon_id: int, item_id: str, category: int
) -> LayerResponse:

    polygon_obj = await Polygon.get_or_none(id=polygon_id)
    if not polygon_obj:
        raise HTTPException(status_code=404, detail="Polygon not found")

    existing_item = await get_existing_layer(
        metric_id, polygon_id, category, item_id
    )
    if existing_item:
        return LayerResponse(layer=existing_item.layer_url)

    categories, values, colors = fetch_collection_metadata(metric_id)

    raster_href = get_asset_href_by_item_id(metric_id, item_id)

    image_base64 = crop_raster(
        raster_path=raster_href,
        polygon=polygon_obj.geometry,
        category=category,
        values=values,
        colors=colors,
    )

    image_url = await upload_to_s3(
        image_data=image_base64,
        filename=f"{metric_id}_{polygon_id}_{item_id}_{category}.png",
        content_type="image/png",
    )

    await save_layer_record(
        metric=metric_id,
        polygon_id=polygon_id,
        category=category,
        item_id=item_id,
        image_url=image_url,
    )

    return LayerResponse(layer=image_url)
