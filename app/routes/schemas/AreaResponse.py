from pydantic import BaseModel

from app.routes.schemas.AreaTypeResponse import AreaTypeResponse
from app.routes.schemas.PolygonRequest import geojson_polygon


class AreaResponse(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {"example": {"id": 1, "name": "Area example"}}


class AreaDetailsResponse(BaseModel):
    id: int
    name: str
    area: float
    area_type: AreaTypeResponse
    geometry: object

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


class PolygonIdResponse(BaseModel):
    polygon_id: int

    class Config:
        json_schema_extra = {"example": {"polygon_id": 1}}
