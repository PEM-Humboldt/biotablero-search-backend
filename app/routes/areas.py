import fastapi
import app.services.area_types as area_types_service
import app.services.areas as area_service

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.AreaResponse import AreaResponse, AreaDetailsResponse
from typing import Annotated, List

router = fastapi.APIRouter(
    prefix="/areas",
    tags=["areas"],
    responses={
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


async def area_id_param(
    area_id: Annotated[
        int, fastapi.Query(description="Area identifier", example="1")
    ],
):
    return area_id


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
async def get_area_details(id: Annotated[int, fastapi.Depends(area_id_param)]):
    """
    Returns area details filtered by identifier.
    """
    return await area_service.get_area_details(id)
