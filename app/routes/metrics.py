import typing
import fastapi
from fastapi import Depends, Body, HTTPException
from geojson_pydantic import Feature, Polygon
from pydantic import BaseModel, Field
from geojson_pydantic import Feature

<<<<<<< Updated upstream
from app.routes.schemas.polygon import (
    PolygonRequest,
    FeatureRequest,
    WrappedFeatureRequest,
)
=======
>>>>>>> Stashed changes
from app.services.metrics import Metrics as metrics_service
from logging import getLogger
from app.services.utils import context_vars

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
    metric_id: typing.Annotated[
        typing.Literal["LossPersistence", "Coverage"],
        fastapi.Path(description="Metric you wish to query"),
    ]
) -> str:
    return metric_id


async def defined_areas_params(
    area_type: typing.Annotated[
        str,
        fastapi.Query(description="type of the predefined area", example="ea"),
    ],
    area_id: typing.Annotated[
        str, fastapi.Query(description="id of the area", example="CAR")
    ],
):
    return {"area_type": area_type, "area_id": area_id}


@router.get("/{metric_id}/areas", response_model=typing.List[AreasResponse])
async def get_areas_by_defined_area(
    metric_id: typing.Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: typing.Annotated[
        dict, fastapi.Depends(defined_areas_params)
    ],
) -> list[dict[str, float]]:
    """
    Given a metric and a predefined area of interest, get the area values for each category in the metric inside the indicated area
    """
    return [
        {"key": "Perdida", "value": 2035},
        {"key": "Persistencia", "value": 40843},
        {"key": "No bosque", "value": 207122},
    ]


@router.post("/{metric_id}/areas", response_model=typing.List[AreasResponse])
async def get_areas_by_polygon(
<<<<<<< Updated upstream
    metric_id: str,
    polygon: typing.Union[FeatureRequest, WrappedFeatureRequest],
    metric_id_param: str = fastapi.Depends(metric_id_param),
) -> typing.List[AreasResponse]:
=======
    metric_id: Annotated[str, Depends(metric_id_param)],
    feature: Annotated[Feature, Body(...)],
) -> List[AreasResponse]:
>>>>>>> Stashed changes
    """
    Given a metric and a polygon, get the area values for each category in the metric inside the polygon
    """
    try:
<<<<<<< Updated upstream
        if isinstance(polygon, WrappedFeatureRequest):
            geometry = polygon.polygon.geometry
        else:
            geometry = polygon.geometry

        # Validación adicional si se desea
        if geometry.bbox is None:
            raise ValueError("Bounding box (bbox) is required in geometry.")

        # Lógica para obtener áreas basadas en el polígono
        return [
            {"key": "Perdida", "value": 2035},
            {"key": "Persistencia", "value": 40843},
            {"key": "No bosque", "value": 207122},
        ]

    except ValueError as ve:
        raise fastapi.HTTPException(status_code=400, detail=str(ve))
=======
        print(feature)
        geometry = feature.geometry  # Accede a la geometría del Feature

        data = metrics_service.get_areas_by_polygon(
            geometry.dict()  # Usa la geometría del Feature
        )
        return data
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except ConnectionError as ce:
        raise HTTPException(
            status_code=503, detail=f"Service unavailable: {ce}"
        )
>>>>>>> Stashed changes
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {e}"
        )


@router.get("/{metric_id}/layer")
async def get_layer_by_defined_area(
    metric_id: typing.Annotated[str, fastapi.Depends(metric_id_param)],
    defined_area: typing.Annotated[
        dict, fastapi.Depends(defined_areas_params)
    ],
):  # TODO: Define return type
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    return {"layer": "response to be defined"}


@router.post(
    "/{metric_id}/areas/defined", response_model=typing.List[AreasResponse]
)
async def get_areas_by_predefined_polygon(
    metric_id: str,
    polygon: typing.Union[FeatureRequest, WrappedFeatureRequest],
    metric_id_param: str = fastapi.Depends(metric_id_param),
) -> typing.List[AreasResponse]:
    """
    Given a metric and a predefined polygon, get the area values for each category in the metric inside the polygon
    """
    try:
        # Validación del bbox utilizando la función importada
        if polygon.geometry.bbox is None:
            raise ValueError("Bounding box (bbox) is required in geometry.")

        # Lógica para obtener áreas basadas en el polígono
        data = metrics_service.get_areas_by_polygon(polygon.model_dump())
        return data
    except ValueError as ve:
        raise fastapi.HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@router.post("/{metric_id}/layer")
async def get_layer_by_polygon(
<<<<<<< Updated upstream
    metric_id: typing.Annotated[str, fastapi.Depends(metric_id_param)],
    polygon: FeatureRequest,
=======
    metric_id: Annotated[str, fastapi.Depends(metric_id_param)],
    feature: Annotated[Feature, Body(...)],
>>>>>>> Stashed changes
):
    """
    Given a metric and a predefined area of interest, get the layer of the metric cut by the indicated area
    """
    logger = getLogger(__name__)
    try:
        logger.info(f"Processing request for metric_id: {metric_id}")
        geometry = feature.geometry

        raster_bytes = metrics_service.get_layer_by_polygon(
<<<<<<< Updated upstream
            metric_id, polygon.model_dump()
=======
            metric_id["metric_id"], geometry.dict()
>>>>>>> Stashed changes
        )

        return fastapi.Response(content=raster_bytes, media_type="image/png")

    except Exception as e:
        logger.error(
            f"Execution error: {e}",
            extra={"request_id": request_id_context.get()},
        )
        raise fastapi.HTTPException(status_code=500, detail=str(e))
