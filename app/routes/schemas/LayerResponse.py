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


class LayerWithBboxResponse(BaseModel):
    """
    Response model used to return the URL and bbox of a generated image layer for visualization
    """

    layer: str
    bbox: tuple[int, int, int, int]

    class Config:
        json_schema_extra = {
            "example": {
                "layer": "http://localhost:4556/eads345.../layer",
                "bbox": [
                    -79.00757596899996,
                    -4.228886820867842,
                    -66.84332596899996,
                    12.458363179132157,
                ],
            }
        }
