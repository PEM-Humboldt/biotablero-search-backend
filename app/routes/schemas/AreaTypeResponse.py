from pydantic import BaseModel


class AreaTypeResponse(BaseModel):
    id: str
    label: str

    class Config:
        json_schema_extra = {
            "example": {"id": "states", "label": "Departamentos"}
        }
