from typing import List
from app.routes.schemas.AreaResponse import AreaResponse
from app.models.models import Polygon, AreaType
from app.utils.config import TORTOISE_ORM
from tortoise import Tortoise


async def get_areas_by_type(area_type_id: str) -> List[AreaResponse]:
    await Tortoise.init(config=TORTOISE_ORM)

    areas = []
    area_type = await AreaType.get_or_none(id=area_type_id)

    if area_type != None:
        area_db_dict = await Polygon.filter(area_type=area_type).values(
            "id", "name"
        )
        areas = [AreaResponse(**area) for area in area_db_dict]

    await Tortoise.close_connections()

    return areas
