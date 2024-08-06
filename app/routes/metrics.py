from typing import Annotated, Literal, List, Any

import fastapi
from pydantic import BaseModel, Field

from app.routes.schemas.polygon import Polygon
from app.services.metrics import Metrics as metrics_service
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


class AreasResponse(BaseModel):
    key: str = Field(
        description="Name or Id of the property", example="Perdida"
    )
    value: float = Field(description="Value of the property", example=2035)


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
):
    return {"metric_id": metric_id}


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


@router.get("/{metric_id}/areas", response_model=List[AreasResponse])
async def get_areas_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
) -> list[dict[str, float]]:
    """
    Given a metric and a predefined area of interest, get the area values for each category in the metric inside the indicated area
    """
    return [
        {"key": "Perdida", "value": 2035},
        {"key": "Persistencia", "value": 40843},
        {"key": "No bosque", "value": 207122},
    ]


@router.post("/{metric_id}/areas", response_model=List[AreasResponse])
async def get_areas_by_polygon(
    metric_id: str,
    polygon: Polygon
) -> dict[str, Any]:
    """
    Given a metric and a polygon, get the area values for each category in the metric inside the polygon.
    """
    try:
        polygon_geometry = polygon.polygon.geometry
        data = metrics_service.get_areas_by_polygon(polygon_geometry, metric_id)
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
    metric_id: str,
    polygon: Polygon,
):
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    logger = getLogger(__name__)
    try:
        polygon_geometry = polygon.polygon.geometry
        raster_bytes = metrics_service.get_layer_by_polygon(
            metric_id,
            polygon_geometry
        )
        return fastapi.Response(content=raster_bytes, media_type="image/png")
    except Exception as e:
        logger.error(
            f"Execution error: {e}",
            extra={"request_id": request_id_context.get()},
        )
        raise fastapi.HTTPException(status_code=500, detail=str(e))
