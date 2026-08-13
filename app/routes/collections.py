from typing import List

from fastapi import APIRouter

import app.services.collections as collection_service

from app.routes.schemas.CollectionResponse import CollectionResponse

router = APIRouter(
    prefix="/collections",
    tags=["collections"],
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


@router.get("", response_model=List[CollectionResponse])
async def get_collections():
    """
    Returns the list of available collections.
    """
    return await collection_service.get_collections()
