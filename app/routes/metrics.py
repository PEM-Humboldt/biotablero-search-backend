from typing import Annotated, Literal, List
import fastapi

from app.routes.schemas.polygon import Polygon
from app.routes.schemas.MetricValues import MetricResponse
import app.services.metrics as metrics_service
from logging import getLogger
from app.utils import context_vars

request_id_context = context_vars.request_id_context

validation_error_example = {
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "polygon"],
            "msg": "Field required",
            "input": {},
        }
    ]
}


router = fastapi.APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={
        404: {"description": "Not found"},
        422: {
            "content": {
                "application/json": {"example": validation_error_example}
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
    try:
        polygon_geometry = polygon.polygon.geometry
        data = metrics_service.get_areas_by_polygon(
            metric_id, polygon_geometry
        )
        return data
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@router.get("/{metric_id}/layer")
async def get_layer_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
):  # TODO: Define return type
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    return {"layer": "response to be defined"}


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
    logger = getLogger(__name__)
    try:
        polygon_geometry = polygon.polygon.geometry
        raster_bytes = metrics_service.get_layer_by_polygon(
            metric_id, polygon_geometry, item_id
        )
        return fastapi.Response(content=raster_bytes, media_type="image/png")
    except Exception as e:
        logger.error(
            f"Execution error: {e}",
            extra={"request_id": request_id_context.get()},
        )
        raise fastapi.HTTPException(status_code=500, detail=str(e))
