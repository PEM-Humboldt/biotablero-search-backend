from typing import TypedDict, Type, List
from pydantic import BaseModel


class LossPersistenceResponse(BaseModel):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    periodo: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0


class CoverageResponse(BaseModel):
    """
    Response model for land cover metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0


class HumanTraceResponse(BaseModel):
    """
    Response model for Human Trace metrics in a given year.
    """

    ano: str = ""
    natural: float = 0
    baja: float = 0
    media: float = 0
    alta: float = 0


class MetricConfig(TypedDict):
    model: Type[BaseModel]
    example: List[dict]
    description: str
    group_key: str
