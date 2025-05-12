from typing import Annotated, Literal, List
import fastapi
from fastapi import Query

from app.routes.schemas.PolygonRequest import PolygonRequest
from app.routes.schemas.MetricResponse import MetricResponse, LayerResponse
import app.services.metrics as metrics_service
from app.services.polygon_metric_service import get_or_create_polygon_metric


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


async def defined_areas_params(
    area_type: Annotated[
        str,
        fastapi.Query(description="type of the predefined area", example="ea"),
    ],
    area_id: Annotated[
        str, fastapi.Query(description="id of the area", example="CAR")
    ],
):
    return {"area_type": area_type, "area_id": area_id}


@router.get("/{metric_id}/values/{id}", response_model=List[MetricResponse])
async def get_values_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    id: int,
) -> List[MetricResponse]:
    """
    Retrieves metric values for a given polygon.

    If the values for the specified metric and polygon already exist in the database,
    they are returned. This endpoint assumes that the values already exist and
    will not create new entries if missing.
    """
    return await get_or_create_polygon_metric(id, metric_id)


@router.get("/{metric_id}/layer")
async def get_layer_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
) -> LayerResponse:  # TODO: Define return type
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    return LayerResponse(layer="response to be defined")


@router.post("/{metric_id}/layer")
async def get_layer_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: PolygonRequest,
    item_id: Annotated[
        str,
        fastapi.Query(
            description="The ID of the item to retrieve",
            example="2016-2021",
        ),
    ],
    category: Annotated[
        int,
        Query(
            description="Category to filter (0: Loss, 1: Persistence, 2: Non-Forest)",
            example=0,
        ),
    ],
) -> LayerResponse:
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    polygon_geometry = polygon.polygon.geometry

    layer = metrics_service.get_layer_by_polygon(
        metric_id, polygon_geometry, item_id, category
    )

    return LayerResponse(layer=layer)
