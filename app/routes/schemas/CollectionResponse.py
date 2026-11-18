from pydantic import BaseModel


class CollectionResponse(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {"example": {"id": 1, "name": "Coberturas"}}
