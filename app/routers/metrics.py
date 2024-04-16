from fastapi import APIRouter

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{metric_id}/areas")
async def get_areas():
    return [{"Perdida": 2035}, {"Persistencia": 40843}, {"No bosque": 207122}]


@router.get("/{metric_id}/layer")
async def get_layer(metric_id):
    return {"layer": "format to be defined"}
