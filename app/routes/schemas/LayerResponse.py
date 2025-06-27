from pydantic import BaseModel


class LayerResponse(BaseModel):
    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer": "http://localhost:4556/eads345.../layer"}
        }
