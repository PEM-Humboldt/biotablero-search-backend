from typing import List, Annotated
from fastapi import APIRouter, Query, Path

from app.routes.schemas.CollectionResponse import CollectionResponse
from app.routes.schemas.LayerResponse import LayerWithBboxResponse

import app.services.collections as collection_service

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
async def get_collections() -> List[CollectionResponse]:
    """
    Returns the list of available collections.
    """
    return await collection_service.get_collections()


@router.get("/{collection_id}/layer", response_model=LayerWithBboxResponse)
async def get_collection_layer(
    collection_id: Annotated[
        int,
        Path(
            description=("Collection id to query"),
            examples=[1],
        ),
    ],
    value: Annotated[
        int,
        Query(
            description=("Value associated to the desired layer"),
            examples=[1130],
        ),
    ],
) -> LayerWithBboxResponse:
    """
    Returns the url of rendered image layer for a given collection, polygon ID, and value.
    """
    img_url, bbox = await collection_service.get_or_create_collection_layer(
        collection_id, value
    )

    return LayerWithBboxResponse(layer=img_url, bbox=bbox)
