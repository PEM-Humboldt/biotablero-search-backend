from pydantic import BaseModel
from typing import Union


class LossPersistenceResponse(BaseModel):
    perdida: float
    persistencia: float
    no_bosque: float
    periodo: str


# dict is temporal because of the type checking, remove after adding another type
MetricResponse = Union[LossPersistenceResponse, dict]
