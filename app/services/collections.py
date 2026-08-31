from typing import List, Tuple
from fastapi import HTTPException

import app.persistence.collection_persistence as collection_persistence
from app.persistence.collection_layer_persistence import (
    get_existing_layer,
    create_collection_layer,
)
from app.persistence.utils.lock_utils import advisory_xact_lock
from app.routes.schemas.CollectionResponse import CollectionResponse
from app.services.utils.raster import generate_image_for_value
from app.services.utils.stac import (
    fetch_collection_metadata,
    get_items_asset_url,
)
from app.utils.s3_utils import upload_to_s3


async def get_collections() -> List[CollectionResponse]:
    """
    Returns id, name of the available collections
    """
    collections_db = await collection_persistence.list_collections()
    collections = [
        CollectionResponse.model_validate(coll) for coll in collections_db
    ]

    return collections


async def get_or_create_collection_layer(
    collection_id: int, value: int
) -> Tuple[str, Tuple[float, float, float, float]]:
    """
    Checks if the layer already exists. If not, generates it, save it and returns the URL.
    """

    collection_obj = await collection_persistence.get_collection_by_id(
        collection_id
    )

    if not collection_obj:
        raise HTTPException(status_code=404, detail="Collection not found")

    async with advisory_xact_lock(
        "collection_layer",
        str(collection_id),
        str(value),
    ) as connection:
        existing_layer = await get_existing_layer(
            collection_obj, value, db=connection
        )

        if existing_layer:
            return existing_layer.layer_url, existing_layer.bbox

        _, values, _, colors, _ = await fetch_collection_metadata(
            collection_obj
        )

        items_raster_href = get_items_asset_url(collection_obj.name)

        image_base64, bbox = generate_image_for_value(
            raster_path=items_raster_href[0][1],
            class_value=value,
            values=values,
            colors=colors,
        )

        image_url = await upload_to_s3(
            image_data=image_base64,
            filename=f"{collection_id}_{value}.png",
            content_type="image/png",
        )

        await create_collection_layer(
            collection=collection_obj,
            value=value,
            image_url=image_url,
            bbox=bbox,
            db=connection,
        )

        return image_url, bbox
