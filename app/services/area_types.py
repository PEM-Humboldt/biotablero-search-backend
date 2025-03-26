from typing import List
from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.models.models import AreaType
from app.utils.config import TORTOISE_ORM
from tortoise import Tortoise


async def get_all() -> List[AreaTypeResponse]:
    await Tortoise.init(config=TORTOISE_ORM)

    area_type_db_dict = await AreaType.all().values("id", "label")
    area_types = [AreaTypeResponse(**area) for area in area_type_db_dict]

    await Tortoise.close_connections()

    return area_types
