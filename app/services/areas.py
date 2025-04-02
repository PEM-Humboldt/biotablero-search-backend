from typing import List
from app.routes.schemas.AreaResponse import AreaResponse, AreaDetailsResponse
from app.models.models import Polygon, AreaType
from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
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


async def get_area_details(id: int) -> AreaDetailsResponse | None:
    await Tortoise.init(config=TORTOISE_ORM)

    area = None
    area_db = await Polygon.filter(id=id).prefetch_related("area_type").first()

    if area_db != None:
        area = AreaDetailsResponse(
            id=area_db.id,
            name=area_db.name,
            area=area_db.area,
            geometry=area_db.geometry,
            area_type=AreaTypeResponse(
                id=area_db.area_type.id if area_db.area_type else "",
                label=area_db.area_type.label if area_db.area_type else "",
            ),
        )

    await Tortoise.close_connections()

    return area
