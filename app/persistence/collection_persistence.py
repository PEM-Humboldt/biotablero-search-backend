from typing import List, Dict
from app.models.models import Collection


async def list_collections() -> List[Dict[str, int | str]]:
    """
    List Collections with basic information.
    """
    return await Collection.all().values("id", "name")


async def get_collection_by_id(
    collection_id: int,
) -> Collection | None:
    """
    Get Collection object by id.
    """
    return await Collection.get_or_none(id=collection_id)
