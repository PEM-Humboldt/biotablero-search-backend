from app.models.models import Collection, CollectionLayer
from app.utils.errors import ServerError
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import IntegrityError


async def get_existing_layer(
    collection: Collection,
    value: int,
    db: BaseDBAsyncClient | None = None,
):
    query = CollectionLayer.filter(collection=collection, value=value)
    if db is not None:
        query = query.using_db(db)
    return await query.first()


async def create_collection_layer(
    collection: Collection,
    value: int,
    image_url: str,
    db: BaseDBAsyncClient | None = None,
):
    create_kwargs = {}
    if db is not None:
        create_kwargs["using_db"] = db
    try:
        await CollectionLayer.create(
            collection=collection,
            value=value,
            layer_url=image_url,
            **create_kwargs,
        )
    except IntegrityError as e:
        raise ServerError(
            code=500,
            usr_msg="There was an error saving the metric layer.",
            e=e,
        ) from e
