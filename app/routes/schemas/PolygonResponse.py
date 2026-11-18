from pydantic import BaseModel


class PolygonIdResponse(BaseModel):
    polygon_id: int

    class Config:
        json_schema_extra = {"example": {"polygon_id": 1}}
