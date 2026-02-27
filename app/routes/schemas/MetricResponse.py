from typing import Union
from pydantic import BaseModel, Field


class BaseMetricResult(BaseModel):
    id: str

    model_config = {"extra": "forbid"}  # prevents unexpected fields


class LossPersistenceResponse(BaseMetricResult):
    """
    Response model for forest loss and persistence metrics in a given period.
    """

    Perdida: float
    Persistencia: float
    No_Bosque: float = Field(alias="No Bosque")

    model_config = {"populate_by_name": True}


class CoverageResponse(BaseMetricResult):
    """
    Response model for land cover metrics in a given year.
    """

    Natural: float
    Secundaria: float
    Transformada: float


class CurrentHFResponse(BaseMetricResult):
    """
    Response model for Human Footprint metrics in a given year.
    """

    Natural: float
    Baja: float
    Media: float
    Alta: float
    Muy_Alta: float = Field(alias="Muy Alta")


class CurrentHFAverageResponse(BaseMetricResult):
    """
    Response model for Human Footprint average in a given year.
    """

    Average: float


class paramoResponse(BaseMetricResult):
    """
    Response model for paramos area in a given year.
    """

    Paramo: float


class tropicalDryForestResponse(BaseMetricResult):
    """
    Response model for tropical dry forest area in a given year.
    """

    BosqueSeco: float


class wetlandResponse(BaseMetricResult):
    """
    Response model for wetland area in a given year.
    """

    Humedal: float


MetricResponse = Union[
    LossPersistenceResponse,
    CoverageResponse,
    CurrentHFResponse,
    CurrentHFAverageResponse,
    paramoResponse,
    tropicalDryForestResponse,
    wetlandResponse,
]
