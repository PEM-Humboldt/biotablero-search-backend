import fastapi
import app.services.area_types as area_types_service

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from typing import List

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


@router.get("/types", response_model=List[AreaTypeResponse])
async def get_all_types() -> List[AreaTypeResponse]:
    """
    Returns all area types.
    """
    return await area_types_service.get_all()
