from pydantic import BaseModel
from typing import Union

class LossPersistenceResponse(BaseModel):
    perdida: float
    persistencia: float
    no_bosque: float
    periodo: str

MetricResponse = Union[LossPersistenceResponse]
