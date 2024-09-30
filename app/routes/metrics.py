from typing import Annotated, Literal, List, Dict, Optional
import fastapi
from pydantic import BaseModel

from app.routes.schemas.polygon import Polygon
from app.routes.schemas.MetricValues import MetricResponse
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
    ]
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


@router.post("/{metric_id}/values", response_model=List[MetricResponse])
async def get_values_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: Polygon,
) -> List[MetricResponse]:
    """
    Given a metric and a polygon, get the area values for each category in the metric inside the polygon.
    """
    polygon_geometry = polygon.polygon.geometry
    data = metrics_service.get_areas_by_polygon(metric_id, polygon_geometry)
    return data


@router.get("/{metric_id}/layer")
async def get_layer_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
):  # TODO: Define return type
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    return {"layer": "response to be defined"}


class LayerResponse(BaseModel):
    images: Dict[
        str, Optional[str]
    ]  # Las claves son cadenas, los valores pueden ser cadenas o None


@router.post("/{metric_id}/layer")
async def get_layer_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: Polygon,
    item_id: Annotated[
        str,
        fastapi.Query(
            description="The ID of the item to retrieve",
            example="example_item_id",
        ),
    ],
):
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    polygon_geometry = polygon.polygon.geometry
    base64_images = metrics_service.get_layer_by_polygon(
        metric_id, polygon_geometry, item_id
    )
    return LayerResponse(images=base64_images)
