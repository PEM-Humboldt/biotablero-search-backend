from typing import List
from app.routes.schemas.AreaType import AreaType as AreaTypeDTO
from app.models.models import AreaType
from app.utils.config import TORTOISE_ORM
from tortoise import Tortoise


async def get_all() -> List[AreaTypeDTO]:
    await Tortoise.init(config=TORTOISE_ORM)

    area_type_db_dict = await AreaType.all().values("id", "label")
    area_types = [AreaTypeDTO(**area) for area in area_type_db_dict]

    await Tortoise.close_connections()

    return area_types
