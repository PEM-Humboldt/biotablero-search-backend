from pydantic import BaseModel


class LayerResponse(BaseModel):
    """
    Response model used to return the URL of a generated image layer for visualization
    """

    layer: str

    class Config:
        json_schema_extra = {
            "example": {"layer": "http://localhost:4556/eads345.../layer"}
        }
