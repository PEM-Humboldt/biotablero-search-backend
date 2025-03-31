from pydantic import BaseModel


class AreaResponse(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {
            "example": {"id": 1, "name": "Area example"}
        }
