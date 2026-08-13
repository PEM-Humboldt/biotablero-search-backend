from typing import Sequence, Dict
from app.models.models import Collection


async def list_collections():
    """
    List Collections with basic information.
    """
    return await Collection.all().values("id", "name")
