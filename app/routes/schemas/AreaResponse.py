from pydantic import BaseModel

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.polygon import geojson_polygon


class AreaResponse(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {"example": {"id": 1, "name": "Area example"}}


class AreaDetailsResponse(BaseModel):
    id: int
    name: str
    area: float
    geometry: object
    # area_type: AreaTypeResponse

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Area example",
                "area": 1.0,
                "geometry": {"polygon": geojson_polygon},
                "area_type": {"id": "states", "label": "Departamentos"},
            }
        }
