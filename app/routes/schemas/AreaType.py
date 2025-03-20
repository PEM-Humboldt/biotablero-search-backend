from pydantic import BaseModel, Field
from typing import Union


class AreaType(BaseModel):
    id: str
    label: str

    class Config:
        json_schema_extra = {
            "example": {"id": "states", "label": "Departamentos"}
        }
