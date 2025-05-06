from app.persistence.polygon_persistence import get_polygon, create_polygon
from app.routes.schemas.PolygonRequest import PolygonRequest
from app.routes.schemas.PolygonResponse import PolygonIdResponse


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
