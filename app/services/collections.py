from typing import List
import app.persistence.collection_persistence as collection_persistence

from app.routes.schemas.CollectionResponse import CollectionResponse


async def get_collections() -> List[CollectionResponse]:
    collections_db = await collection_persistence.list_collections()
    collections = [CollectionResponse(**coll) for coll in collections_db]

    return collections
