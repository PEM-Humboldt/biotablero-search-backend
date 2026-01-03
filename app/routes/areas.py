from typing import List

from fastapi import APIRouter, HTTPException

import app.services.area_types as area_types_service
import app.services.areas as area_service

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.AreaResponse import AreaResponse, AreaDetailsResponse
from app.routes.schemas.PolygonRequest import PolygonRequest
from app.routes.schemas.PolygonResponse import PolygonIdResponse

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


@router.post("/polygon", response_model=PolygonIdResponse)
async def create_or_get_polygon(
    polygon: PolygonRequest,
) -> PolygonIdResponse:
    """
    Receives a polygon . If polygon exists (by hash), return its ID.
    If not, create it and return the new ID.
    """
    return await area_service.get_or_create_polygon(polygon)
