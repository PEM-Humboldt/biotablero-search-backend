from typing import Annotated, Literal, List
import fastapi
from fastapi import Query

from app.routes.schemas.MetricResponse import (
    MetricResponse,
    LayerResponse,
    MetricResponseBase,
)
import app.services.metrics as metrics_service

validation_error_example = {
    "detail": [
        {
            "loc": ["body", "polygon"],
            "msg": "Field required",
            "type": "value_error.missing",
        }
    ]
}

router = fastapi.APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={
        404: {"description": "Not found"},
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {"example": validation_error_example}
            },
        },
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


async def metric_id_param(
    metric_id: Annotated[
        Literal["LossPersistence", "Coverage"],
        fastapi.Path(description="metric you whish to query"),
    ],
) -> str:
    return metric_id


@router.get(
    "/{metric_id}/values/{id}",
    response_model=MetricResponse,
)
async def get_values_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    id: int,
) -> List[MetricResponseBase]:
    """Returns metric values for a polygon identified by its ID."""
    return await metrics_service.get_or_create_polygon_metric(id, metric_id)


@router.get("/{metric_id}/layer", response_model=LayerResponse)
async def get_layer_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon_id: Annotated[int, Query(description="Polygon ID to use")],
    item_id: Annotated[
        str, Query(description="The ID of the item", example="2016-2021")
    ],
    category: Annotated[
        int,
        Query(
            description=(
                "Numeric code representing a classification category used to differentiate types of land cover or change. "
                "For example: 0 = Loss (deforested areas), 1 = Persistence (stable forest), 2 = Non-Forest (non-forest areas)."
            ),
            example=0,
        ),
    ],
):
    """
    Returns the url of rendered image layer for a given metric, polygon ID, item ID, and category,
    typically used to visualize spatial data such as forest loss, persistence, or non-forest areas.
    """
    return await metrics_service.get_or_create_layer_by_polygon(
        metric_id, polygon_id, item_id, category
    )
