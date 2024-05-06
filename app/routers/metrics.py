from typing import Annotated, Literal
import fastapi
from .polygon import Polygon

router = fastapi.APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
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


# TODO: Successful response examples for /areas
# TODO: 422 response examples for /areas and /layer


@router.get("/{metric_id}/areas")
async def get_areas_by_defined_area(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: Annotated[dict, fastapi.Depends(defined_areas_params)],
) -> list[dict[str, float]]:
    """
    Given a metric and a predefined area of interest, get the area values for each category in the metric inside the indicated area
    """
    return [
        {"Perdida": 2035, "Persistencia": 40843, "No bosque": 207122},
    ]


@router.post("/{metric_id}/areas")
async def get_areas_by_polygon(
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: Polygon,
) -> list[dict[str, float]]:  # TODO: Define return type
    """
    Given a metric and a polygon, get the area values for each category in the metric inside the polygon
    """
    return [
        {"Perdida": 2035, "Persistencia": 40843, "No bosque": 207122},
    ]


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
):
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    return {"layer": "response to be defined"}
