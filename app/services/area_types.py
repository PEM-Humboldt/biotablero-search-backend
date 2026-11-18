from typing import List
from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.models.models import AreaType


async def get_all() -> List[AreaTypeResponse]:

    area_type_db_dict = await AreaType.all().values("id", "label")
    area_types = [AreaTypeResponse(**area) for area in area_type_db_dict]

    return area_types
