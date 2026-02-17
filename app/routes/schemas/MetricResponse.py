from typing import Dict, TypedDict, Type, List
from pydantic import BaseModel


class LossPersistenceResponse(BaseModel):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    id: str = ""
    perdida: float = 0
    persistencia: float = 0
    no_bosque: float = 0


class CoverageResponse(BaseModel):
    """
    Response model for land cover metrics in a given year.
    """

    id: str = ""
    natural: float = 0
    secundaria: float = 0
    transformada: float = 0


class CurrentHFResponse(BaseModel):
    """
    Response model for Human Footprint metrics in a given year.
    """

    id: str = ""
    natural: float = 0
    baja: float = 0
    media: float = 0
    alta: float = 0


class CurrentHFAverageResponse(BaseModel):
    """
    Response model for Human Footprint mean in a given year.
    """

    id: str = ""
    mean: float = 0


class MetricConfig(TypedDict):
    model: Type[BaseModel]
    example: List[dict] | Dict
    description: str
