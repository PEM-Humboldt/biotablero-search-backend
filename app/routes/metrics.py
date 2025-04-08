from typing import Annotated, Literal, List
import fastapi
from fastapi import Query

from app.routes.schemas.PolygonRequest import PolygonRequest
from app.routes.schemas.MetricResponse import (
    MetricResponse,
    LayerResponse,
    PolygonResponse,
)
import app.services.metrics as metrics_service
from app.services.utils import polygon_validate

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


@router.get("/{metric_id}/values", response_model=List[MetricResponse])
async def get_values_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
) -> List[MetricResponse]:
    """
    Given a metric and a predefined area of interest, get the area values for each category in the metric inside the indicated area
    """
    area_type = defined_area["area_type"]
    area_id = defined_area["area_id"]
    return metrics_service.get_areas_by_defined_area(
        metric_id, area_type, area_id
    )


@router.post("/{metric_id}/values", response_model=List[PolygonResponse])
async def get_values_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: PolygonRequest,
) -> List[PolygonResponse]:
    """
    Given a metric and a polygon, get the area values for each category in the metric inside the polygon.
    """
    polygon_geometry = polygon.polygon.geometry
    area_raw = metrics_service.get_areas_by_polygon(
        metric_id, polygon_geometry
    )
    area_dicts = polygon_validate.serialize_area_data(area_raw)
    area_total = polygon_validate.extract_total_area_from_last_period(
        area_dicts
    )
    polygon_id = await polygon_validate.get_or_create_polygon(
        polygon_geometry, metric_id, area_total, area_dicts
    )

    return [PolygonResponse(id=polygon_id)]


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
