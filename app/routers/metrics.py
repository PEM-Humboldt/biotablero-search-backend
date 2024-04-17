from typing import Annotated
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)


# TODO: This must be a post request
@router.get("/{metric_id}/areas")
async def get_areas(
    metric_id: str,
    polygon: Annotated[str | None, Query(max_length=1)] = None,
):
    return [
        {"Perdida": 2035},
        {"Persistencia": 40843},
        {"No bosque": 207122},
    ]


# TODO: This must be a post request


@router.get("/{metric_id}/layer")
async def get_layer(metric_id: str):
    return {"layer": "format to be defined"}


# Validaciones del polígono
# Deshabilitar el tryout en modo producción del swagger
