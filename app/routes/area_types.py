import fastapi
import app.services.area_types as area_types_service

from app.routes.schemas.AreaType import AreaType
from typing import List

router = fastapi.APIRouter(
    prefix="/area_types",
    tags=["area_types"],
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

@router.get("types", response_model=List[AreaType])
async def get_all_values() -> List[AreaType]:
    """
    Returns all area types.
    """
    return await area_types_service.get_all()