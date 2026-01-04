from typing import List
from tortoise import Tortoise

from app.routes.schemas.AreaResponse import AreaResponse, AreaDetailsResponse
from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.PolygonRequest import PolygonRequest
from app.routes.schemas.PolygonResponse import PolygonIdResponse

from app.models.models import Polygon, AreaType
from app.persistence.polygon_persistence import get_polygon, create_polygon


async def get_areas_by_type(area_type_id: str) -> List[AreaResponse]:
    areas = []
    area_type = await AreaType.get_or_none(id=area_type_id)

    if area_type != None:
        area_db_dict = await Polygon.filter(area_type=area_type).values(
            "id", "name"
        )
        areas = [AreaResponse(**area) for area in area_db_dict]

    return areas


async def get_area_details(id: int) -> AreaDetailsResponse | None:
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

    return area


async def get_or_create_polygon(
    polygon: PolygonRequest,
) -> PolygonIdResponse:
    """
    Checks if a polygon already exists in the database by comparing its geometry.
    If it exists, returns the corresponding polygon ID.
    If it does not exist, creates a new polygon record and returns the new ID.
    """
    polygon_geometry = polygon.polygon.geometry

    existing_id = await get_polygon(polygon_geometry)
    if existing_id is not None:
        return PolygonIdResponse(polygon_id=existing_id)

    created_id = await create_polygon(polygon_geometry)
    return PolygonIdResponse(polygon_id=created_id)
