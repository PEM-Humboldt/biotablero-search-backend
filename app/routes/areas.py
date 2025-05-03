from fastapi import APIRouter, HTTPException, Depends
import app.services.area_types as area_types_service
import app.services.areas as area_service
from app.routes.metrics import metric_id_param

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.AreaResponse import (
    AreaResponse,
    AreaDetailsResponse,
    PolygonIdResponse,
)
from typing import List, Annotated

from app.routes.schemas.PolygonRequest import PolygonRequest
from app.services import polygon_service

router = APIRouter(
    prefix="/areas",
    tags=["areas"],
    responses={
        404: {"description": "Not found"},
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "An internal server error occurred."
                    }
                },
            },
        },
    },
)


@router.get("/types", response_model=List[AreaTypeResponse])
async def get_all_types() -> List[AreaTypeResponse]:
    """
    Returns all area types.
    """
    return await area_types_service.get_all()


@router.get("", response_model=List[AreaResponse])
async def get_areas_by_type(type: str):
    """
    Returns areas filtered by type.
    """
    return await area_service.get_areas_by_type(type)


@router.get("/{id}", response_model=AreaDetailsResponse)
async def get_area_details(id: int):
    """
    Returns area details filtered by identifier.
    """
    response = await area_service.get_area_details(id)

    if response == None:
        raise HTTPException(status_code=404, detail="Not found")

    return response


@router.post("/polygon/{metric_id}", response_model=PolygonIdResponse)
async def create_or_get_polygon(
    metric_id: Annotated[str, Depends(metric_id_param)],
    polygon: PolygonRequest,
) -> PolygonIdResponse:
    """
    Receives a polygon and a metric ID. If polygon exists (by hash), return its ID.
    If not, create it and return the new ID.
    """
    polygon_geometry = polygon.polygon.geometry
    existing_id = await polygon_service.polygon_exists(polygon_geometry)
    if existing_id is not None:
        return PolygonIdResponse(polygon_id=existing_id)

    created_id = await polygon_service.create_polygon(
        polygon_geometry, metric_id
    )
    return PolygonIdResponse(polygon_id=created_id)
